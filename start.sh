#!/bin/bash
# Start KeyAssist

cd "$(dirname "$0")"

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "⚠️  Ollama is not running!"
    echo "Please start it with: ollama serve"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

# Activate virtual environment and run
source venv/bin/activate
python keyassist.py
