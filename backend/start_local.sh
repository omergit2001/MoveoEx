#!/bin/bash

echo "Starting Crypto Dashboard Backend..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo ""
    echo "WARNING: .env file not found!"
    echo "Please copy .env.example to .env and configure it."
    echo ""
    read -p "Press enter to continue anyway..."
fi

# Start the server
echo ""
echo "Starting Flask server on http://localhost:5000"
echo "Press Ctrl+C to stop"
echo ""
python run.py

