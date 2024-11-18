# Frequently Asked Questions (FAQ) ❓

## Quick Answers

### 🎯 About the Study

**Q: What exactly am I doing here?**
> You're helping us understand how developers really work! Just code normally and share your thoughts along the way.

**Q: How long will this take?**
> 1-2 hours total, but you can split it up however you like. Take breaks!

**Q: Do I need to be an expert?**
> Not at all! We want developers of all levels. Your experience is valuable no matter what.

### 🛠️ Technical Stuff

**Q: Help! The code isn't working!**
```bash
# Try these first:
git pull origin main  # Get latest updates
pip install -r requirements.txt  # Fresh install
```
> Still stuck? Drop us a message!

**Q: Can I use my own IDE/tools?**
> Absolutely! Use whatever makes you comfortable.

**Q: What if I get stuck on the coding task?**
> That's totally fine! The task is just a prompt - we care more about your experience than the solution.

### 📝 Sharing Your Experience

**Q: What should I write about?**
> Anything that comes to mind:
> - 💭 Your thought process
> - 🛠️ How you use your tools
> - 😤 What frustrates you
> - 🎉 What works well

**Q: Do I have to use all the input methods?**
> Nope! Use whatever feels natural:
> - ✍️ Writing
> - 🎙️ Voice notes
> - 🎨 Sketches
> - 📸 Screenshots
> - Whatever works for you!

**Q: What if I don't have much to say?**
> Short answers are fine! Quality over quantity.

### 🔒 Privacy & Data

**Q: Who sees my responses?**
> Only the research team. We keep everything anonymous.

**Q: What happens to my code?**
> It stays in your branch. We look at your process, not judge your code.

**Q: Can I skip questions?**
> Absolutely! Share only what you're comfortable with.

### 🤝 Getting Help

**Q: I have a question not covered here!**
> We're here to help:
> - 💬 Discord: [link]
> - 📧 Email: [address]
> - 🐛 GitHub Issues

**Q: Can I suggest improvements?**
> Yes please! Open an issue or PR.

## Still Have Questions? 💁‍♀️
Don't hesitate to reach out. We're here to help!

## Data Collection & Privacy

### What data do you collect?
> We collect only what you explicitly provide:
> - Your reflection responses
> - Code examples you choose to share
> - Optional system information (OS, Python version)
> - Submission timestamps
> All data collection is transparent and configurable.

### Can I see what data is being collected?
> Yes! All your data is stored locally in `.probe_responses/`. You can:
> - Review all files before submission
> - Check the generated PDF summary
> - Verify file checksums
> - See exactly what's included in the submission package

### Why are some files protected?
> We protect certain files to:
> - Maintain research integrity
> - Prevent accidental modifications
> - Ensure consistent templates
> You can still view all protected files and temporarily unprotect them if needed.

## Technical Questions

### How do I submit my responses?
> 1. Complete your reflections in `.probe_responses/`
> 2. Run `python submit_probes.py` in `04_submission/`
> 3. Review the generated PDF
> 4. Email the submission package manually

### What if I need to modify a protected file?
> Use the protection manager in your code:
> ```python
> with protection_manager.temporarily_unprotect(path):
>     # Make your changes here
> ```

### How do I know my submission is complete?
> The submission process includes:
> - ✅ Checksum verification
> - ✅ PDF summary generation
> - ✅ QR code for verification
> - ✅ List of included files
> Review the PDF before sending!

## Research & Purpose

### How will my data be used?
> Your data helps us:
> - Understand developer workflows
> - Improve development tools
> - Advance software engineering research
> All data is anonymized and used only for research purposes.

### Can I withdraw from the study?
> Yes, you can:
> - Choose not to submit your responses
> - Request data deletion after submission
> - Opt-out at any time
> Contact us at elric.ettmueller@hm.edu

### What makes this different from other studies?
> Our approach:
> - Respects your privacy
> - Gives you control over your data
> - Uses transparent collection methods
> - Maintains research integrity
> - Provides clear documentation

## Configuration & Customization

### Can I customize the submission format?
> Yes! Edit `probe_config.yaml` to:
> - Enable/disable system info collection
> - Configure PDF formatting
> - Set security preferences
> - Customize email templates

### What security features are available?
> - SHA-256 checksums
> - File protection
> - Manual submission control
> - PDF watermarking
> - QR code verification

### Can I use my own templates?
> Yes, but:
> - Keep original templates as reference
> - Ensure consistent formatting
> - Document any modifications
> - Follow the provided structure

## Support & Contact

### I found a bug, what should I do?
> 1. Check if it's a known issue
> 2. Create a detailed bug report
> 3. Include steps to reproduce
> Contact: elric.ettmueller@hm.edu

### How do I get help?
> - 📖 Read the documentation
> - 💬 Open an issue on GitHub
> - 📧 Email: [address]
> - 🌐 Check our website

### Can I contribute to the project?
> Yes! You can:
> - Report bugs
> - Suggest improvements
> - Share your experience
> See `CONTRIBUTING.md` for guidelines
