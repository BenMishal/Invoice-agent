```bash
# 1. Clone repo and install dependencies
git clone <your-repo>
cd invoice-agent
python -m venv venv
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt

# 2. Set environment variables
cp .env.example .env
# Edit .env with your credentials

# 3. Test individual agents
python -m pytest tests/test_agents.py

# 4. Run API locally
python api/main.py

# 5. Test API endpoint
curl -X POST http://localhost:8080/api/v1/invoices/process \
  -F "file=@sample_invoice.pdf" \
  -F "vendor_name=Acme Corp"

# 6. Deploy to Cloud Run
gcloud run deploy invoice-agent \
  --source . \
  --platform managed \
  --region us-central1
```