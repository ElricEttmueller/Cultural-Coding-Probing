# Git Workflow for Cultural Probes 🔄

## Overview

This document explains how to work with this repository as a research participant. The workflow is designed to be simple and maintain privacy for your responses.

## Important ❗

- **DO NOT** create pull requests
- **DO NOT** push your changes back to the repository
- **DO NOT** fork the repository publicly if you want to keep your responses private

## Workflow Steps 📝

### 1. Getting Started

```bash
# Clone the repository
git clone https://github.com/your-org/cultural-probes.git
cd cultural-probes

# Create a new branch for your work (optional, for your local organization)
git checkout -b my-responses
```

### 2. Working with the Repository

Your work and responses will be stored in:
- `.probe_responses/` - Your research responses
- `03_reflection/reflections/` - Your reflections
- `03_reflection/diary/` - Your diary entries

These directories are already in `.gitignore` to prevent accidental commits.

### 3. Submitting Your Work

**DO NOT** submit your work through Git. Instead:

1. Use the provided submission tool:
   ```bash
   python 04_submission/submit_probes.py
   ```

2. This will:
   - Create a PDF summary of your responses
   - Package your submissions securely
   - Generate verification checksums
   - Prepare for email submission

3. Follow the email submission instructions provided by the tool

### 4. Privacy Protection 🔒

- Your responses stay local until you choose to submit
- Protected directories prevent accidental modifications
- Submission process is manual and under your control
- No automatic Git pushes or pulls

### 5. Updating the Framework

If you need to get updates to the framework:

```bash
# Save your current changes to a different location if needed
# Then update your local copy
git fetch origin
git reset --hard origin/main
```

⚠️ **Warning**: This will overwrite any changes to framework files, but your responses in ignored directories will be safe.

### 6. Common Questions ❓

Q: Should I commit my changes?
A: No, your responses should not be committed to Git.

Q: How do I update the framework?
A: Use `git fetch` and `git reset` as shown above.

Q: What if I want to keep a backup of my responses?
A: Manually copy the `.probe_responses` directory to a secure location.

### 7. Need Help? 🆘

If you encounter any issues:
1. Check the FAQ.md file
2. Review the README.md
3. Contact the research team
4. DO NOT open GitHub issues for response-related questions

## Remember 🎯

This is a research tool designed to:
- Protect your privacy
- Collect genuine insights
- Maintain data integrity
- Support your reflection process

Your responses are valuable research data, but they should remain private until you choose to submit them through the proper channels.
