"""Capture Agent - Enhanced with improved Gemini prompts"""
import logging
import base64
import json
import re
from pathlib import Path
from typing import Dict, Any
import google.generativeai as genai

logger = logging.getLogger(__name__)

class CaptureAgent:
    """Enhanced agent for capturing invoice data with high accuracy"""
    
    def __init__(self, model_name: str = "gemini-2.0-flash"):
        self.model = genai.GenerativeModel(model_name)
        self.model_name = model_name
    
    def encode_image(self, image_path: str) -> str:
        """Encode image to base64"""
        with open(image_path, "rb") as image_file:
            return base64.standard_b64encode(image_file.read()).decode("utf-8")
    
    def is_handwritten_document(self, file_path: str) -> bool:
        """Detect if document is handwritten"""
        file_ext = Path(file_path).suffix.lower()
        return file_ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    
    def get_handwriting_extraction_prompt(self) -> str:
        """Enhanced prompt for handwritten invoices"""
        return """You are an expert invoice data extractor. Extract the following fields from the invoice image.
Return ONLY valid JSON. Do not include markdown formatting like ```json ... ```.

RULES:
1. Extract values exactly as they appear.
2. If a field is missing, use null.
3. Convert dates to YYYY-MM-DD format if possible.
4. Extract amounts as numbers (e.g. 1234.56).
5. For currency, look for symbols ($, €, £) or codes (USD, EUR, GBP). Default to null if unsure.

FIELDS TO EXTRACT:
- invoice_number: The invoice identifier (e.g., INV-001)
- vendor_name: The name of the vendor/company
- invoice_date: The date of the invoice
- due_date: The payment due date
- total_amount: The total amount to be paid
- tax_amount: The tax amount
- currency: The currency code (USD, EUR, GBP, etc.)
- payment_terms: Payment terms (e.g., Net 30)
- extraction_confidence: high/medium/low

JSON OUTPUT:
{
    "invoice_number": null,
    "vendor_name": null,
    "invoice_date": null,
    "due_date": null,
    "total_amount": null,
    "tax_amount": null,
    "currency": null,
    "payment_terms": null,
    "extraction_confidence": "high"
}"""
    
    def get_digital_extraction_prompt(self) -> str:
        """Enhanced prompt for digital PDFs"""
        return """You are an expert invoice data extractor. Extract the following fields from the invoice PDF.
Return ONLY valid JSON. Do not include markdown formatting like ```json ... ```.

RULES:
1. Extract values exactly as they appear.
2. If a field is missing, use null.
3. Convert dates to YYYY-MM-DD format if possible.
4. Extract amounts as numbers (e.g. 1234.56).
5. For currency, look for symbols ($, €, £) or codes (USD, EUR, GBP). Default to null if unsure.

FIELDS TO EXTRACT:
- invoice_number: The invoice identifier (e.g., INV-001)
- vendor_name: The name of the vendor/company
- invoice_date: The date of the invoice
- due_date: The payment due date
- total_amount: The total amount to be paid
- tax_amount: The tax amount
- currency: The currency code (USD, EUR, GBP, etc.)
- payment_terms: Payment terms (e.g., Net 30)
- extraction_confidence: high/medium/low

JSON OUTPUT:
{
    "invoice_number": null,
    "vendor_name": null,
    "invoice_date": null,
    "due_date": null,
    "total_amount": null,
    "tax_amount": null,
    "currency": null,
    "payment_terms": null,
    "extraction_confidence": "high"
}"""
    
    def extract_from_handwritten_invoice(self, file_path: str) -> Dict[str, Any]:
        """Extract from handwritten invoice"""
        logger.info(f"🖊️ Handwritten: {file_path}")
        
        try:
            image_data = self.encode_image(file_path)
            prompt = self.get_handwriting_extraction_prompt()
            
            # CORRECT Gemini API format with proper MIME type
            response = self.model.generate_content([
                {
                    "mime_type": "image/jpeg",
                    "data": image_data
                },
                prompt
            ])
            
            extracted_json = self._parse_response(response.text)
            
            logger.info(f"✅ Success")
            
            return {
                "status": "success",
                "document_type": "handwritten",
                "extracted_data": extracted_json,
                "model": self.model_name
            }
            
        except Exception as e:
            logger.error(f"❌ Error: {str(e)}")
            return {
                "status": "error",
                "document_type": "handwritten",
                "error": str(e),
                "model": self.model_name
            }
    
    def extract_from_digital_invoice(self, file_path: str) -> Dict[str, Any]:
        """Extract from digital PDF"""
        logger.info(f"📄 Digital: {file_path}")
        
        try:
            with open(file_path, "rb") as pdf_file:
                pdf_data = base64.standard_b64encode(pdf_file.read()).decode("utf-8")
            
            prompt = self.get_digital_extraction_prompt()
            
            # CORRECT Gemini API format with proper MIME type
            response = self.model.generate_content([
                {
                    "mime_type": "application/pdf",
                    "data": pdf_data
                },
                prompt
            ])
            
            extracted_json = self._parse_response(response.text)
            
            logger.info(f"✅ Success")
            
            return {
                "status": "success",
                "document_type": "digital",
                "extracted_data": extracted_json,
                "model": self.model_name
            }
            
        except Exception as e:
            logger.error(f"❌ Error: {str(e)}")
            return {
                "status": "error",
                "document_type": "digital",
                "error": str(e),
                "model": self.model_name
            }
    
    def _parse_response(self, response_text: str) -> Dict:
        """Parse JSON with improved handling for markdown blocks"""
        # Strip markdown code blocks if present
        text = response_text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
        
        try:
            data = json.loads(text)
            return self._clean_data(data)
        except json.JSONDecodeError:
            # Try regex fallback if direct parse fails
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                try:
                    data = json.loads(json_match.group(0))
                    return self._clean_data(data)
                except json.JSONDecodeError:
                    pass
        
        logger.warning(f"Could not parse JSON from response: {response_text[:100]}...")
        return self._fallback_extraction(response_text)
        
        logger.warning("Could not parse JSON")
        return self._fallback_extraction(response_text)
    
    def _clean_data(self, data: Dict) -> Dict:
        """Clean data but be less aggressive about removing values"""
        # Only remove values that are clearly placeholders or empty
        placeholders = ['not found', 'tbd', 'to be determined', 'unknown']
        
        cleaned = {}
        for key, value in data.items():
            if value is None:
                cleaned[key] = None
                continue
                
            if isinstance(value, str):
                # Check for placeholders
                if any(p == value.lower().strip() for p in placeholders):
                    cleaned[key] = None
                elif value.strip() == '':
                    cleaned[key] = None
                else:
                    cleaned[key] = value
            else:
                cleaned[key] = value
        
        return cleaned
    
    def _fallback_extraction(self, text: str) -> Dict:
        """Fallback extraction"""
        return {
            "invoice_number": None,
            "vendor_name": None,
            "invoice_date": None,
            "due_date": None,
            "total_amount": None,
            "tax_amount": None,
            "currency": "USD",
            "extraction_confidence": "low"
        }
    
    def capture(self, invoice_path: str) -> Dict[str, Any]:
        """Main capture method"""
        logger.info(f"🔄 Capturing: {invoice_path}")
        
        if self.is_handwritten_document(invoice_path):
            return self.extract_from_handwritten_invoice(invoice_path)
        else:
            return self.extract_from_digital_invoice(invoice_path)
