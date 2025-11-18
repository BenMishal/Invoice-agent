#!/bin/bash
# ============================================================================
# SETUP SCRIPT - Complete Project Setup
# Save as: setup.sh
# Usage: ./setup.sh
# ============================================================================

echo "================================"
echo "Invoice Agent - Project Setup"
echo "================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "✅ Python version: $python_version"
echo ""

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
echo "✅ pip upgraded"
echo ""

# Install requirements
echo "Installing requirements..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "✅ Requirements installed"
else
    echo "❌ requirements.txt not found!"
    exit 1
fi
echo ""

# Check .env file
if [ -f ".env" ]; then
    echo "✅ .env file exists"
    if grep -q "GEMINI_API_KEY" .env; then
        echo "✅ GEMINI_API_KEY found in .env"
    else
        echo "⚠️  GEMINI_API_KEY not found in .env"
        echo "Please add: GEMINI_API_KEY=your-api-key"
    fi
else
    echo "⚠️  .env file not found"
    echo "Creating .env template..."
    cat > .env << 'EOF'
# Google AI
GEMINI_API_KEY=your-gemini-api-key-here
DEFAULT_MODEL=gemini-2.0-flash-exp

# Google Cloud
GOOGLE_CLOUD_PROJECT=your-project-id

# API Configuration
API_HOST=0.0.0.0
API_PORT=8080
ENVIRONMENT=development
LOG_LEVEL=INFO
EOF
    echo "✅ .env template created"
    echo "Please edit .env and add your API keys"
fi
echo ""

# Create necessary directories
echo "Creating project directories..."
mkdir -p agents
mkdir -p api
mkdir -p tests/sample_invoices
echo "✅ Directories created"
echo ""

# Test imports
echo "Testing agent imports..."
python -c "
try:
    from agents.orchestrator import InvoiceOrchestrator
    from agents.capture_agent import InvoiceCaptureAgent
    from agents.validation_agent import ValidationAgent
    from agents.routing_agent import RoutingAgent
    from agents.optimizer_agent import OptimizationAgent
    from agents.exception_handler import ExceptionHandlerAgent
    print('✅ All agents imported successfully')
except ImportError as e:
    print('⚠️  Import error:', e)
    print('Make sure all agent files are in place')
"
echo ""

# Summary
echo "================================"
echo "Setup Complete!"
echo "================================"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your GEMINI_API_KEY"
echo "2. Run: ./start-api.sh to start the server"
echo "3. Run: ./test-api.sh to test endpoints"
echo ""
