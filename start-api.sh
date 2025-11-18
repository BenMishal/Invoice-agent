#!/bin/bash
# ============================================================================
# QUICK START SCRIPT - Start API Server
# Save as: start-api.sh
# Usage: ./start-api.sh
# ============================================================================

echo "================================"
echo "Starting Invoice Agent API"
echo "================================"
echo ""

# Navigate to project directory
cd "$(dirname "$0")"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please create one first: python -m venv venv"
    exit 1
fi

# Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Make sure GEMINI_API_KEY is set in environment"
fi

# Start API server
echo "✅ Starting API server on port 8080..."
echo "   Press Ctrl+C to stop"
echo ""
python api/main.py
