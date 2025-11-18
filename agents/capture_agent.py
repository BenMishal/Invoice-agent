import google.generativeai as genai
from typing import Dict, Any
import os
import json
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class InvoiceCaptureAgent:
    def __init__(self):
        self.model_name = os.getenv("DEFAULT_MODEL", "gemini-2.0-flash-exp")
        logger.info(f"✅ Initializing Capture Agent")
        genai.configure(***REMOVED***os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel(self.model_name)
        logger.info("✅ Capture Agent created")
    
    def extract(self, pdf_path: str) -> Dict[str, Any]:
        try:
            logger.info(f"📄 Extracting from: {pdf_path}")
            prompt = f"""Extract invoice data from: {pdf_path}
Return JSON with: invoice_number, vendor_name, invoice_date, due_date, amount_total, currency, tax_amount, payment_terms"""
            
            response = self.model.generate_content(prompt)
            return {"status": "success", "extracted_data": response.text}
        except Exception as e:
            logger.error(f"❌ Error: {e}")
            return {"status": "error", "error": str(e)}