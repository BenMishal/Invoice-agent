import google.generativeai as genai
from typing import Dict, Any
import os
import json
from dotenv import load_dotenv
import logging
from PIL import Image  

load_dotenv()
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class InvoiceCaptureAgent:
    def __init__(self):
        self.model_name = os.getenv("DEFAULT_MODEL", "gemini-1.5-flash")
        logger.info(f"✅ Initializing Capture Agent")
        genai.configure(***REMOVED***os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel(self.model_name)
        logger.info("✅ Capture Agent created")
    
    def extract_handwritten(self, image_path: str) -> Dict[str, Any]:
        """Extract data from handwritten invoice"""
        try:
            logger.info(f"📝 Extracting from handwritten: {image_path}")
            
            # Load image
            image = Image.open(image_path)
            
            prompt = """This is a handwritten invoice. Extract ALL information accurately:

REQUIRED FIELDS:
- Invoice number
- Vendor/Supplier name  
- Invoice date
- Due date
- Total amount
- Currency
- Tax/VAT amount
- Payment terms
- Line items (description, quantity, price)

INSTRUCTIONS:
- Read handwriting carefully
- Parse dates correctly (YYYY-MM-DD format)
- Convert handwritten numbers to digits
- Handle crossed-out corrections
- Note any unclear fields

Return structured JSON with all extracted data."""
            
            # Call Gemini with image
            response = self.model.generate_content([prompt, image])
            
            return {
                "status": "success",
                "extracted_data": response.text,
                "source_type": "handwritten",
                "confidence": "varies by handwriting quality"
            }
            
        except Exception as e:
            logger.error(f"❌ Error extracting handwritten: {e}")
            return {"status": "error", "error": str(e)}
    
    def extract(self, pdf_path: str) -> Dict[str, Any]:
        """Original extract method for digital PDFs"""
        try:
            logger.info(f"📄 Extracting from: {pdf_path}")
            
            # Check file type
            if pdf_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                # Image file - use handwritten extraction
                return self.extract_handwritten(pdf_path)
            
            prompt = f"""Extract invoice data from: {pdf_path}
Return JSON with: invoice_number, vendor_name, invoice_date, due_date, amount_total, currency, tax_amount, payment_terms"""
            
            response = self.model.generate_content(prompt)
            return {"status": "success", "extracted_data": response.text}
        except Exception as e:
            logger.error(f"❌ Error: {e}")
            return {"status": "error", "error": str(e)}
