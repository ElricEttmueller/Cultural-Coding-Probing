# Cultural Probes for Software Development Research 🔍

## Overview

This is a research tool designed to collect qualitative data about software development practices in a privacy-respecting, transparent manner. It's part of a research study conducted at Munich University of Applied Sciences.

## What This Tool Does

This framework helps:
- 📝 Collect your development experiences through structured reflections
- 🔒 Securely package and submit your responses
- 📊 Preserve privacy while gathering valuable research data

## How It Works

### 1. Data Collection
- Your responses are stored locally in `.probe_responses/`
- Only you can access and review your data before submission
- Certain directories are protected to prevent accidental modifications

### 2. Submission Process
- Creates a verifiable PDF summary
- Packages responses with checksums
- Includes optional system information
- Generates QR codes for verification

### 3. Privacy & Security
- All data collection is transparent
- You control what data to submit
- No automatic uploads
- Manual email submission process
- File integrity verification

## Getting Started

1. **Setup**
   ```bash
   pip install -r requirements.txt
   ```

2. **Directory Structure**
   - `02_your_task/`: Task descriptions and examples
   - `03_reflection/`: Templates for reflections
   - `.probe_responses/`: Your responses
   - `04_submission/`: Submission tools

3. **Configuration**
   Edit `probe_config.yaml` to customize:
   - Email settings
   - Security preferences
   - Submission format
   - File protection rules

## Your Privacy Rights

- ✅ View all collected data
- ✅ Modify your responses before submission
- ✅ Choose what system info to include
- ✅ Review the final package
- ✅ Manual submission control

## File Protection

Some directories are protected to maintain research integrity:
- Example solutions
- Templates
- Submitted responses

To modify protected files:
```python
with protection_manager.temporarily_unprotect(path):
    # Make your changes
```

## Submission Guide

1. **Prepare Responses**
   - Complete reflection templates
   - Review your responses
   - Ensure all files are saved

2. **Generate Submission**
   ```bash
   cd 04_submission
   python submit_probes.py
   ```

3. **Review & Submit**
   - Check the generated PDF
   - Verify included files
   - Send to: elric.ettmueller@hm.edu

## Technical Details

- Python 3.8+ required
- Uses ReportLab for PDF generation
- SHA-256 checksums for verification
- Configurable watermarking
- QR code verification

## Need Help?

- 📖 Check `FAQ.md` for common questions
- 💬 Open an issue for technical problems
- 📧 Contact: elric.ettmueller@hm.edu

## Research Context

This tool is part of a study on software development practices. Your participation helps:
- Understand developer workflows
- Improve development tools
- Enhance software engineering education

## Acknowledgments

Thank you for participating in our research! Your insights help advance our understanding of software development practices.

## License

MIT License - See LICENSE file for details
