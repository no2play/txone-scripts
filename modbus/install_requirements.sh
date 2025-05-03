#!/bin/bash

echo "🔍 Checking for Python 3..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.8 or later."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

echo "📁 Creating virtual environment (env)..."
python3 -m venv env

echo "⚙️ Activating virtual environment..."
source env/bin/activate

echo "📦 Installing required packages..."
pip install --upgrade pip
pip install pymodbus

echo "✅ Installation complete!"
echo "👉 To activate the environment next time, run: source env/bin/activate"
