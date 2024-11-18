#!/usr/bin/env python3

import os
import yaml
import zipfile
import datetime
import hashlib
import platform
import json
import pyqrcode
import markdown
import tempfile
from pathlib import Path
from typing import Dict, Any
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, 
    PageBreak, Table, TableStyle, Flowable, Preformatted
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER

class Watermark(Flowable):
    """Adds a watermark to PDF pages."""
    def __init__(self, text):
        Flowable.__init__(self)
        self.text = text
        
    def draw(self):
        canvas = self.canv
        canvas.saveState()
        canvas.setFont('Helvetica', 70)
        canvas.setFillColor(colors.lightgrey)
        canvas.setFillAlpha(0.3)
        canvas.translate(letter[0]/2, letter[1]/2)
        canvas.rotate(45)
        canvas.drawCentredString(0, 0, self.text)
        canvas.restoreState()

class ProbeSubmission:
    def __init__(self, config_path: str = "../probe_config.yaml"):
        """Initialize submission handler with configuration."""
        self.config_path = Path(config_path).resolve()
        self.config = self._load_config()
        
        # Set up directories relative to the config file location
        config_dir = self.config_path.parent
        self.response_dir = (config_dir / self.config['directories']['responses']).resolve()
        self.output_dir = (config_dir / self.config['directories']['submissions']).resolve()
        self.template_dir = (config_dir / self.config['directories']['templates']).resolve()
        
        # Create necessary directories
        self.output_dir.mkdir(exist_ok=True)
        self.template_dir.mkdir(exist_ok=True)
        
        # Generate submission ID
        self.submission_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    def _load_config(self) -> Dict:
        """Load probe configuration from YAML file."""
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)

    def _generate_qr_code(self, data: str) -> str:
        """Generate QR code for submission verification."""
        qr = pyqrcode.create(data)
        temp_path = tempfile.mktemp(suffix='.png')
        qr.png(temp_path, scale=5)
        return temp_path

    def _calculate_checksum(self, file_path: Path) -> str:
        """Calculate SHA-256 checksum of a file."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def _get_system_info(self) -> Dict[str, str]:
        """Collect system information."""
        return {
            "os": platform.system(),
            "os_version": platform.version(),
            "machine": platform.machine(),
            "python_version": platform.python_version(),
            "timestamp": datetime.datetime.now().isoformat()
        }

    def _create_submission_zip(self) -> str:
        """Create an encrypted ZIP file containing all probe responses."""
        zip_path = self.output_dir / f"probe_submission_{self.submission_id}.zip"
        
        # Count response files before zipping
        response_files = list(self.response_dir.glob('*.md'))
        if not response_files:
            raise ValueError("No probe responses found in .probe_responses directory")
            
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add probe responses
            for file_path in response_files:
                if file_path.is_file() and not file_path.name.startswith('.'):
                    print(f"   Adding response: {file_path.name}")
                    zipf.write(file_path, file_path.relative_to(self.response_dir))
            
            # Add submission metadata
            metadata = {
                'submission_id': self.submission_id,
                'timestamp': datetime.datetime.now().isoformat(),
                'num_responses': len(response_files),
                'response_files': [f.name for f in response_files],
                'system_info': self._get_system_info() if self.config['submission_settings']['submission_format']['include_system_info'] else {},
                'config': self.config
            }
            
            metadata_path = self.output_dir / 'submission_metadata.json'
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            zipf.write(metadata_path, 'submission_metadata.json')
            metadata_path.unlink()

        # Calculate checksum if enabled
        if self.config['submission_settings']['security']['generate_checksum']:
            self.checksum = self._calculate_checksum(zip_path)
            
        return zip_path

    def _create_submission_pdf(self, zip_path: Path) -> str:
        """Create a comprehensive PDF report of all probe responses."""
        pdf_path = self.output_dir / f"probe_submission_{self.submission_id}.pdf"
        
        # Create PDF document
        doc = SimpleDocTemplate(
            str(pdf_path),
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Get styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER
        )
        heading_style = styles['Heading2']
        normal_style = styles['Normal']
        
        # Create document content
        content = []
        
        # Add watermark if enabled
        if self.config['submission_settings']['pdf_settings']['watermark']:
            content.append(Watermark(self.config['submission_settings']['pdf_settings']['watermark']))
        
        # Add cover page if enabled
        if self.config['submission_settings']['pdf_settings']['include_cover_page']:
            content.append(Paragraph(self.config['submission_settings']['metadata']['research_project'], title_style))
            content.append(Spacer(1, 0.5*inch))
            
            # Add institution info
            content.append(Paragraph(self.config['submission_settings']['metadata']['institution'], heading_style))
            content.append(Spacer(1, 0.25*inch))
            
            # Add submission details table
            submission_data = [
                ['Submission ID:', self.submission_id],
                ['Timestamp:', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
                ['Number of Responses:', str(len(list(self.response_dir.glob('*.md'))))],
            ]
            
            if hasattr(self, 'checksum'):
                submission_data.append(['Checksum:', self.checksum])
            
            table = Table(submission_data, colWidths=[2*inch, 4*inch])
            table.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('PADDING', (0, 0), (-1, -1), 6),
            ]))
            content.append(table)
            
            # Add QR code if enabled
            if self.config['submission_settings']['submission_format']['generate_qr']:
                qr_data = f"ID:{self.submission_id}\nChecksum:{getattr(self, 'checksum', 'N/A')}"
                qr_path = self._generate_qr_code(qr_data)
                content.append(Spacer(1, 0.5*inch))
                content.append(Image(qr_path, width=2*inch, height=2*inch))
                
            # Add data handling notice
            content.append(Spacer(1, inch))
            content.append(Paragraph(
                self.config['submission_settings']['metadata']['data_handling_notice'],
                normal_style
            ))
            
            content.append(PageBreak())
        
        # Add responses
        content.append(Paragraph("Probe Responses", heading_style))
        content.append(Spacer(1, 0.25*inch))
        
        for response_file in sorted(self.response_dir.glob('*.md')):
            if response_file.is_file():
                with open(response_file, 'r') as f:
                    md_content = f.read()
                    
                content.append(Paragraph(response_file.name, heading_style))
                content.append(Spacer(1, 0.1*inch))
                
                # Convert markdown to HTML and add content
                html_content = markdown.markdown(md_content)
                content.append(Paragraph(html_content, normal_style))
                content.append(Spacer(1, 0.5*inch))
        
        # Add footer
        content.append(Spacer(1, inch))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER,
            textColor=colors.grey
        )
        
        # Add contact information
        content.append(Paragraph(
            f"Contact: {self.config['submission_settings']['metadata']['contact_info']}",
            footer_style
        ))
        
        # Generate email template
        email_template = self.config['email_template'].format(
            submission_id=self.submission_id,
            timestamp=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            num_responses=len(list(self.response_dir.glob('*.md'))),
            checksum=getattr(self, 'checksum', 'N/A'),
            participant_name="[Your Name]"
        )
        
        content.append(Spacer(1, 0.5*inch))
        content.append(Paragraph("Email Template:", heading_style))
        content.append(Preformatted(email_template, styles['Code']))
        
        # Build PDF
        doc.build(content)
        return pdf_path

    def submit(self) -> bool:
        """Create submission files."""
        try:
            print("Creating submission package...")
            
            # Create ZIP of raw responses
            zip_path = self._create_submission_zip()
            print(f"✅ Created response archive: {zip_path}")
            print(f"   Checksum: {getattr(self, 'checksum', 'N/A')}")
            
            # Create PDF report
            pdf_path = self._create_submission_pdf(zip_path)
            print(f"✅ Created submission PDF: {pdf_path}")
            
            print("\n📤 Submission package created successfully!")
            print(f"📁 Location: {self.output_dir.absolute()}")
            print("\n📧 Next Steps:")
            print("1. Review the generated PDF")
            print(f"2. Email the PDF to: {self.config['submission_settings']['receiver_email']}")
            print("3. Keep the ZIP file for your records")
            print("\nℹ️  The PDF includes a pre-formatted email template you can use.")
            
            return True

        except Exception as e:
            print(f"\n❌ Error during submission: {str(e)}")
            return False

def main():
    """Main entry point for submission script."""
    print("Starting Cultural Probe submission process...")
    
    submission = ProbeSubmission()
    if submission.submit():
        print("\nThank you for participating in our study! 🙏")
    else:
        print("\n❌ Submission failed. Please try again or contact support.")

if __name__ == "__main__":
    main()
