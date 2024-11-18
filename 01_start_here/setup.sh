#!/bin/bash

echo "🚀 Setting up your Cultural Probes environment..."

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3 first."
    exit 1
fi

# Check Git installation
if ! command -v git &> /dev/null; then
    echo "❌ Git not found. Please install Git first."
    exit 1
fi

# Create virtual environment
echo "🔧 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Create participant branch
echo "🌿 Creating your branch..."
read -p "Enter your name (for branch creation): " participant_name
git checkout -b "${participant_name}/probe"

# Create response directories
echo "📁 Setting up your workspace..."
mkdir -p .probe_responses/${participant_name}/{diary,reflections,media}

# Success message
echo """
✨ Setup complete! Here's your next steps:

1. 📝 Read through 01_start_here/README.md
2. 🎯 Choose your task in 02_your_task/
3. 💭 Document your journey
4. 🚀 Submit when ready

Need help? Check FAQ.md or reach out to us!
"""
