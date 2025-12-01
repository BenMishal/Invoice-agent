"""Capture Agent - Enhanced for handwriting and text detection"""
import logging
import base64
from pathlib import Path
from typing import Dict, Any
import google.generativeai as genai

logger = logging.getLogger(__name__)

class CaptureAgent:
    """Agent for capturing and extracting invoice data with handwriting support"""
    
    def __init__(self, model_name: str = "gemini-2.0-flash"):
        self.model = genai.GenerativeModel(model_name)
        self.model_name = model_name
    
    def encode_image(self, image_path: str) -> str:
        """Encode image to base64 for Gemini"""
        with open(image_path, "rb") as image_file:
            return base64.standard_b64encode(image_file.read()).decode("utf-8")
    
    def is_handwritten_document(self, file_path: str) -> bool:
        """Detect if document is handwritten or digital"""
        file_ext = Path(file_path).suffix.lower()
        return file_ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    
    def extract_from_handwritten_invoice(self, file_path: str) -> Dict[str, Any]:
        """Extract data from handwritten invoice image"""
        logger.info(f"🖊️ Detecting handwritten invoice: {file_path}")
        
        try:
            # Encode image
            image_data = self.encode_image(file_path)
            
            # Enhanced prompt for handwriting recognition
            prompt = """You are an expert at reading HANDWRITTEN invoices. Carefully examine this handwritten invoice image and extract ALL invoice details.

IMPORTANT INSTRUCTIONS:
1. Read ALL handwritten text carefully - even if messy or unclear
2. Extract EVERY detail you can see, even partial/unclear text
3. For unclear text, provide your best interpretation
4. Handle cursive and print handwriting
5. Don't skip any fields even if partially visible

EXTRACT THESE FIELDS:
- Invoice Number: [Look for "INV", "No.", "Invoice #", or any number sequence]
- Vendor Name: [Company name at top or "From:" field]
- Invoice Date: [Date written on document]
- Due Date: [Payment due date if visible]
- Amount/Total: [Final total amount]
- Tax: [Tax amount if separate]
- Items: [Line items if visible]
- Payment Terms: [e.g., "Net 30", "Due on receipt"]
- Any other details you can read

OUTPUT FORMAT - Return ONLY valid JSON with no comments:
{
    "document_type": "handwritten_invoice",
    "extraction_confidence": "high/medium/low",
    "invoice_number": "value or null",
    "vendor_name": "value or null",
    "invoice_date": "YYYY-MM-DD or null",
    "due_date": "YYYY-MM-DD or null",
    "total_amount": number or null,
    "tax_amount": number or null,
    "currency": "USD or detected currency",
    "line_items": [{"description": "", "quantity": 0, "amount": 0}],
    "payment_terms": "value or null",
    "notes": "Any additional observations about handwriting clarity",
    "extracted_text": "Full text you could read from the document"
}"""
            
            # Call Gemini with vision capability
            response = self.model.generate_content([
                {
                    "type": "image",
                    "data": image_data
                },
                {
                    "type": "text",
                    "text": prompt
                }
            ])
            
            logger.info(f"✅ Handwritten invoice processed successfully")
            
            return {
                "status": "success",
                "document_type": "handwritten",
                "extracted_data": response.text,
                "model": self.model_name,
                "confidence": "high"
            }
            
        except Exception as e:
            logger.error(f"❌ Error processing handwritten invoice: {str(e)}")
            return {
                "status": "error",
                "document_type": "handwritten",
                "error": str(e),
                "model": self.model_name
            }
    
    def extract_from_digital_invoice(self, file_path: str) -> Dict[str, Any]:
        """Extract data from digital PDF invoice"""
        logger.info(f"📄 Processing digital PDF: {file_path}")
        
        try:
            # Read PDF file
            with open(file_path, "rb") as pdf_file:
                pdf_data = base64.standard_b64encode(pdf_file.read()).decode("utf-8")
            
            # Enhanced prompt for PDF
            prompt = """You are an expert at extracting invoice data from PDF documents. Analyze this invoice PDF and extract ALL relevant information.

INSTRUCTIONS:
1. Read all text in the PDF carefully
2. Extract structured invoice information
3. If a field is not visible, set it to null
4. For amounts, extract numeric values only
5. Format dates consistently as YYYY-MM-DD

EXTRACT THESE FIELDS:
- Invoice Number
- Vendor Name
- Invoice Date
- Due Date
- Total Amount
- Tax Amount
- Subtotal
- Line Items (description, quantity, unit price, amount)
- Payment Terms
- Currency
- Bill To / Customer Info
- Any discounts or additional charges

OUTPUT FORMAT - Return ONLY valid JSON:
{
    "document_type": "digital_invoice",
    "invoice_number": "value or null",
    "vendor_name": "value or null",
    "invoice_date": "YYYY-MM-DD or null",
    "due_date": "YYYY-MM-DD or null",
    "total_amount": number or null,
    "subtotal": number or null,
    "tax_amount": number or null,
    "currency": "USD or detected",
    "line_items": [{"description": "", "quantity": 0, "unit_price": 0, "amount": 0}],
    "payment_terms": "value or null",
    "customer_info": {"name": "", "address": ""},
    "extraction_status": "complete/partial"
}"""
            
            # Call Gemini with PDF
            response = self.model.generate_content([
                {
                    "type": "application/pdf",
                    "data": pdf_data
                },
                {
                    "type": "text",
                    "text": prompt
                }
            ])
            
            logger.info(f"✅ Digital invoice processed successfully")
            
            return {
                "status": "success",
                "document_type": "digital",
                "extracted_data": response.text,
                "model": self.model_name,
                "confidence": "high"
            }
            
        except Exception as e:
            logger.error(f"❌ Error processing digital invoice: {str(e)}")
            return {
                "status": "error",
                "document_type": "digital",
                "error": str(e),
                "model": self.model_name
            }
    
    def capture(self, invoice_path: str) -> Dict[str, Any]:
        """Main capture method - routes to handwriting or digital processing"""
        logger.info(f"🔄 Capturing invoice: {invoice_path}")
        
        # Detect document type
        if self.is_handwritten_document(invoice_path):
            logger.info("🖊️ Detected handwritten document - using OCR mode")
            return self.extract_from_handwritten_invoice(invoice_path)
        else:
            logger.info("📄 Detected digital document - using PDF mode")
            return self.extract_from_digital_invoice(invoice_path)
