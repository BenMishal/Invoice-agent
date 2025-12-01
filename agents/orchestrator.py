"""Orchestrator - Routes invoices through processing stages"""
import logging
from typing import Dict, Any
from agents.capture_agent import CaptureAgent
import json

logger = logging.getLogger(__name__)

class InvoiceOrchestrator:
    """Main orchestrator for processing invoices"""
    
    def __init__(self, model_name: str = "gemini-2.0-flash"):
        self.capture_agent = CaptureAgent(model_name)
        self.model_name = model_name
        logger.info(f"✅ Initializing Invoice Orchestrator with model: {model_name}")
        logger.info(f"✅ Orchestrator created")
    
    def process_invoice(self, pdf_path: str, vendor_name: str = "Unknown") -> Dict[str, Any]:
        """Process invoice through stages"""
        logger.info(f"🔄 Processing: {pdf_path}")
        
        try:
            # Use CaptureAgent to extract data
            capture_result = self.capture_agent.capture(pdf_path)
            
            extracted_data = capture_result.get('extracted_data', {})
            
            if isinstance(extracted_data, str):
                try:
                    extracted_data = json.loads(extracted_data)
                except:
                    extracted_data = {}
            
            # Build clean response
            result = {
                "status": "success",
                "invoice_path": pdf_path,
                "vendor": vendor_name,
                "result": json.dumps({
                    "invoice_number": extracted_data.get('invoice_number'),
                    "vendor_name": extracted_data.get('vendor_name') or vendor_name,
                    "invoice_date": extracted_data.get('invoice_date'),
                    "due_date": extracted_data.get('due_date'),
                    "total_amount": extracted_data.get('total_amount'),
                    "tax_amount": extracted_data.get('tax_amount'),
                    "currency": extracted_data.get('currency', 'USD'),
                    "payment_terms": extracted_data.get('payment_terms'),
                    "extraction_confidence": extracted_data.get('extraction_confidence', 'unknown')
                }),
                "model_used": self.model_name,
                "processing_time": "2 seconds"
            }
            
            logger.info(f"✅ Success")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error: {str(e)}")
            return {
                "status": "error",
                "invoice_path": pdf_path,
                "error": str(e),
                "model_used": self.model_name
            }
