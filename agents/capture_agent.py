from google.adk.agents.llm_agent import Agent
from typing import Dict, Any
import os
import json
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class InvoiceCaptureAgent:
    """Extracts structured data from invoice PDFs using OCR and NLP"""
    
    def __init__(self):
        self.model = os.getenv("DEFAULT_MODEL", "gemini-2.0-flash-exp")
        logger.info(f"✅ Initializing Capture Agent with model: {self.model}")
        try:
            self.agent = Agent(
                name="invoice_capture_agent",
                model=self.model,
                instruction="""You are an expert invoice data extraction specialist.
Your task: Extract ALL invoice data from PDF and return ONLY valid JSON.

EXTRACT THESE FIELDS (REQUIRED):
1. invoice_number - The unique invoice identifier
2. vendor_name - Company name of invoice sender
3. invoice_date - Date invoice was issued (YYYY-MM-DD)
4. due_date - Payment due date (YYYY-MM-DD)
5. amount_total - Total invoice amount (number)
6. currency - Currency code (USD, GBP, EUR, etc.)
7. tax_amount - Tax/VAT amount
8. payment_terms - Terms like "Net 30", "2/10 Net 30"
9. line_items - Array of items with description, quantity, unit_price, amount

EXTRACT THESE FIELDS (OPTIONAL):
10. vendor_email - Vendor contact email
11. vendor_phone - Vendor phone number
12. purchase_order - PO number if available
13. subtotal - Subtotal before tax

FORMATTING RULES:
- If field not found, set to null (NOT empty string)
- For amounts: numeric value only (e.g., 1500.00)
- For dates: convert to YYYY-MM-DD format
- For currency: use ISO 4217 codes
- Extract ALL line items, not just summary
- Return ONLY the JSON object, no explanation text

RETURN VALID JSON ONLY:
{"invoice_number": "string", "vendor_name": "string", "invoice_date": "YYYY-MM-DD", "due_date": "YYYY-MM-DD", "amount_total": 0, "currency": "USD", "tax_amount": 0, "payment_terms": "string", "line_items": [], "vendor_email": null, "vendor_phone": null, "purchase_order": null, "subtotal": 0, "extraction_confidence": 0.95, "extraction_timestamp": "YYYY-MM-DD HH:MM:SS", "quality_notes": []}"""
            )
            logger.info("✅ Capture Agent created successfully")
        except Exception as e:
            logger.error(f"❌ Error creating capture agent: {str(e)}")
            raise
    
    def extract(self, pdf_path: str) -> Dict[str, Any]:
        """Extract invoice data from PDF"""
        try:
            logger.info(f"📄 Extracting data from: {pdf_path}")
            prompt = f"""Extract all invoice data from this PDF file:
File: {pdf_path}
Analyze the PDF content carefully and extract all fields.
Return ONLY valid JSON with extracted data."""
            logger.info("🤖 Calling capture agent...")
            result = self.agent(prompt)
            logger.info("✅ Extraction completed")
            extracted_data = result
            if isinstance(result, str):
                try:
                    extracted_data = json.loads(result)
                    logger.info("✅ Parsed JSON response")
                except json.JSONDecodeError:
                    logger.warning("⚠️  Response is not JSON")
                    extracted_data = {"raw_result": result}
            return {
                "status": "success",
                "extracted_data": extracted_data,
                "pdf_path": pdf_path,
                "model_used": self.model
            }
        except Exception as e:
            logger.error(f"❌ Error extracting invoice: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "error": str(e),
                "pdf_path": pdf_path,
                "error_type": type(e).__name__
            }

if __name__ == "__main__":
    try:
        capture = InvoiceCaptureAgent()
        result = capture.extract("/path/to/sample_invoice.pdf")
        logger.info(json.dumps(result, indent=2, default=str))
    except Exception as e:
        logger.error(f"Test failed: {e}", exc_info=True)