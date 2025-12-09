#!/bin/bash

echo "Starting Crypto Dashboard Frontend..."
echo ""

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo ""
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "Please edit .env and set REACT_APP_API_URL if needed"
    echo ""
fi

# Start the React app
echo ""
echo "Starting React app on http://localhost:3000"
echo "Press Ctrl+C to stop"
echo ""
npm start

