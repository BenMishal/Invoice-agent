#!/bin/bash
# ============================================================================
# INVOICE AGENT - COMPLETE BASH COMMANDS REFERENCE
# Save this file as: invoice-agent-commands.sh
# ============================================================================

# ============================================================================
# 1. PROJECT SETUP COMMANDS
# ============================================================================

# Navigate to project
cd invoice-agent

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Check installed packages
pip list

# ============================================================================
# 2. API SERVER COMMANDS
# ============================================================================

# Start API server (Terminal 1)
python api/main.py

# Start API in background
python api/main.py &

# Start API with specific port
API_PORT=8081 python api/main.py

# Check if port 8080 is in use
lsof -i :8080

# Kill process on port 8080
kill -9 $(lsof -t -i:8080)

# ============================================================================
# 3. TESTING COMMANDS
# ============================================================================

# Test root endpoint
curl http://localhost:8080/

# Test health endpoint
curl http://localhost:8080/health

# Test invoice status endpoint
curl http://localhost:8080/api/v1/invoices/TEST-001/status

# Pretty print JSON response
curl -s http://localhost:8080/ | python -m json.tool

# Test all agents import
python -c "
from agents.orchestrator import InvoiceOrchestrator
from agents.capture_agent import InvoiceCaptureAgent
from agents.validation_agent import ValidationAgent
from agents.routing_agent import RoutingAgent
from agents.optimizer_agent import OptimizationAgent
from agents.exception_handler import ExceptionHandlerAgent
print('✅ All agents imported successfully!')
"

# Run setup test
python test_setup.py

# Run agent tests
python test_agents.py

# Run complete API test
python test_complete.py

# ============================================================================
# 4. GIT COMMANDS
# ============================================================================

# Check git status
git status

# Add all files
git add .

# Commit with message
git commit -m "Your commit message here"

# Push to GitHub
git push origin main

# View commit history
git log --oneline

# Create new branch
git checkout -b feature-branch-name

# Switch back to main
git checkout main

# ============================================================================
# 5. ENVIRONMENT COMMANDS
# ============================================================================

# Check .env file exists
ls -la .env

# View .env contents (be careful - contains secrets!)
cat .env

# Check if GEMINI_API_KEY is set
cat .env | grep GEMINI_API_KEY

# Add variable to .env
echo "NEW_VARIABLE=value" >> .env

# Test environment variable loading
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('GEMINI_API_KEY set:', bool(os.getenv('GEMINI_API_KEY')))
"

# ============================================================================
# 6. FILE MANAGEMENT COMMANDS
# ============================================================================

# List all project files
ls -la

# View project structure
tree -L 2  # Requires tree package

# Check agents directory
ls agents/

# View file contents
cat agents/orchestrator.py

# Count lines of code
find . -name "*.py" -exec wc -l {} + | sort -n

# Check file sizes
du -sh *

# ============================================================================
# 7. SCREEN SESSION COMMANDS (For Background Processes)
# ============================================================================

# Start new screen session
screen -S api-server

# Inside screen: Start API
python api/main.py

# Detach from screen (Press Ctrl+A, then D)
# Or use this command:
screen -d

# List all screen sessions
screen -ls

# Reattach to screen
screen -r api-server

# Kill screen session
screen -X -S api-server quit

# ============================================================================
# 8. DEBUGGING COMMANDS
# ============================================================================

# Check Python version
python --version

# Check which Python is being used
which python

# Test imports individually
python -c "from agents.orchestrator import InvoiceOrchestrator; print('✅')"
python -c "from agents.capture_agent import InvoiceCaptureAgent; print('✅')"
python -c "from agents.validation_agent import ValidationAgent; print('✅')"
python -c "from agents.routing_agent import RoutingAgent; print('✅')"
python -c "from agents.optimizer_agent import OptimizationAgent; print('✅')"
python -c "from agents.exception_handler import ExceptionHandlerAgent; print('✅')"

# Test FastAPI imports
python -c "import fastapi; print('FastAPI version:', fastapi.__version__)"

# Test google-adk import
python -c "import google.adk; print('✅ google-adk imported')"

# Check requirements installed correctly
pip check

# Verify package versions
pip show google-adk
pip show fastapi
pip show pydantic

# ============================================================================
# 9. CLEANUP COMMANDS
# ============================================================================

# Remove __pycache__ directories
find . -type d -name "__pycache__" -exec rm -rf {} +

# Remove .pyc files
find . -name "*.pyc" -delete

# Remove temporary files
rm -rf /tmp/*.pdf

# Clean pip cache
pip cache purge

# ============================================================================
# 10. DOCKER COMMANDS (For Future Deployment)
# ============================================================================

# Build Docker image
docker build -t invoice-agent:latest .

# Run Docker container
docker run -p 8080:8080 invoice-agent:latest

# List running containers
docker ps

# Stop container
docker stop <container-id>

# Remove container
docker rm <container-id>

# View container logs
docker logs <container-id>

# ============================================================================
# 11. GOOGLE CLOUD COMMANDS (For Deployment)
# ============================================================================

# Login to Google Cloud
gcloud auth login

# Set project
gcloud config set project YOUR_PROJECT_ID

# Deploy to Cloud Run
gcloud run deploy invoice-agent \
  --source . \
  --region us-central1 \
  --allow-unauthenticated

# View Cloud Run services
gcloud run services list

# View service logs
gcloud run services logs invoice-agent

# ============================================================================
# 12. UTILITY COMMANDS
# ============================================================================

# Create directory
mkdir -p tests/sample_invoices

# Copy file
cp source_file destination_file

# Move/rename file
mv old_name new_name

# Delete file
rm filename

# Delete directory
rm -rf directory_name

# Create empty file
touch filename

# Edit file with nano
nano filename

# Edit file with vim
vim filename

# Search for text in files
grep -r "search_term" .

# Find files by name
find . -name "*.py"

# ============================================================================
# 13. NETWORK/API TESTING COMMANDS
# ============================================================================

# Test internet connection
ping -c 3 google.com

# Test API with curl (GET)
curl http://localhost:8080/health

# Test API with curl (POST)
curl -X POST http://localhost:8080/api/v1/invoices/process \
  -F "file=@sample.pdf" \
  -F "vendor_name=Test Vendor"

# Download file
wget https://example.com/sample.pdf

# Check open ports
netstat -an | grep LISTEN

# Test DNS resolution
nslookup google.com

# ============================================================================
# 14. MONITORING COMMANDS
# ============================================================================

# Watch API logs
tail -f api.log

# Monitor system resources
top

# Check disk space
df -h

# Check memory usage
free -h

# Monitor network traffic
netstat -an

# ============================================================================
# 15. BACKUP COMMANDS
# ============================================================================

# Backup entire project
tar -czf invoice-agent-backup-$(date +%Y%m%d).tar.gz invoice-agent/

# Extract backup
tar -xzf invoice-agent-backup-20251118.tar.gz

# Backup database (if using)
# pg_dump dbname > backup.sql

# ============================================================================
# 16. QUICK SHORTCUTS
# ============================================================================

# Alias for activating venv + running API
alias start-api='cd invoice-agent && source venv/bin/activate && python api/main.py'

# Alias for running tests
alias test-all='cd invoice-agent && source venv/bin/activate && python test_complete.py'

# Alias for git commit+push
alias gitcp='git add . && git commit -m "Update" && git push'

# ============================================================================
# 17. COMMON WORKFLOWS
# ============================================================================

# Complete startup workflow
startup() {
    cd invoice-agent
    source venv/bin/activate
    python api/main.py
}

# Complete test workflow
test-workflow() {
    cd invoice-agent
    source venv/bin/activate
    python test_setup.py
    python test_agents.py
    python test_complete.py
}

# Deploy workflow
deploy-workflow() {
    git add .
    git commit -m "Deploy: $(date +%Y%m%d-%H%M%S)"
    git push origin main
    gcloud run deploy invoice-agent --source . --region us-central1
}

# ============================================================================
# NOTES
# ============================================================================

# To use this file:
# 1. Save as invoice-agent-commands.sh
# 2. Make executable: chmod +x invoice-agent-commands.sh
# 3. Source it: source invoice-agent-commands.sh
# 4. Or copy individual commands as needed

# Common usage patterns:
# - Use Terminal 1 for API server (keep running)
# - Use Terminal 2 for testing commands
# - Commit often: git add . && git commit -m "message" && git push

# ============================================================================
# END OF FILE
# ============================================================================
