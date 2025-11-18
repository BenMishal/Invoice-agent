import google.generativeai as genai
from typing import Dict, Any, Optional
import os
import json
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class InvoiceOrchestrator:
    def __init__(self):
        self.model_name = os.getenv("DEFAULT_MODEL", "gemini-2.0-flash-exp")
        logger.info(f"✅ Initializing Invoice Orchestrator with model: {self.model_name}")
        genai.configure(***REMOVED***os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel(self.model_name)
        logger.info("✅ Orchestrator created")
    
    def process_invoice(self, pdf_path: str, vendor_name: Optional[str] = None) -> Dict[str, Any]:
        try:
            logger.info(f"🔄 Processing: {pdf_path}")
            prompt = f"""Process invoice: {pdf_path}, Vendor: {vendor_name or 'Unknown'}
STAGE 1 - CAPTURE: Extract invoice data
STAGE 2 - VALIDATE: Check data quality
STAGE 3 - ROUTE: Determine approval path
STAGE 4 - OPTIMIZE: Analyze payment timing
STAGE 5 - EXCEPTION: Handle issues
Return comprehensive JSON."""
            
            response = self.model.generate_content(prompt)
            return {"status": "success", "result": response.text, "pdf_path": pdf_path}
        except Exception as e:
            logger.error(f"❌ Error: {e}")
            return {"status": "error", "error": str(e)}