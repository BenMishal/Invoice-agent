from google.adk.agents.llm_agent import Agent
from typing import Dict, Any, Optional
import os
import json
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class InvoiceOrchestrator:
    """Root orchestrator managing the complete invoice processing pipeline."""
    
    def __init__(self):
        self.model = os.getenv("DEFAULT_MODEL", "gemini-2.0-flash-exp")
        logger.info(f"✅ Initializing Invoice Orchestrator with model: {self.model}")
        try:
            self.orchestrator = Agent(
                name="invoice_orchestrator",
                model=self.model,
                instruction="""You are the invoice processing orchestrator.
You manage the complete flow of invoices through these 5 sequential stages:
STAGE 1 - CAPTURE: Extract structured data from the PDF invoice
STAGE 2 - VALIDATE: Verify data quality and check for duplicates  
STAGE 3 - ROUTE: Determine the approval path based on amount/validation
STAGE 4 - OPTIMIZE: Analyze payment timing and discount opportunities
STAGE 5 - EXCEPTION: Handle any issues and create escalation tickets
For each stage, provide clear context for the next stage.
Maintain complete invoice state throughout the pipeline.
Return a comprehensive JSON response with all decisions and data."""
            )
            logger.info("✅ Orchestrator agent created successfully")
        except Exception as e:
            logger.error(f"❌ Error creating orchestrator: {str(e)}")
            raise
    
    def process_invoice(self, pdf_path: str, vendor_name: Optional[str] = None) -> Dict[str, Any]:
        """Process a single invoice through the complete pipeline."""
        try:
            logger.info(f"🔄 Starting invoice processing: {pdf_path}")
            logger.info(f"   Vendor: {vendor_name or 'Unknown'}")
            prompt = f"""Process this invoice completely through all 5 stages:
FILE: {pdf_path}
VENDOR: {vendor_name or 'Unknown Vendor'}
STAGE 1 - CAPTURE: Extract: invoice_number, vendor_name, invoice_date, due_date, amount_total, currency, tax_amount, payment_terms, line_items. Return: Extracted data in JSON format with extraction_confidence
STAGE 2 - VALIDATE: Check: data completeness, format correctness, duplicate detection, fraud signals, calculation accuracy. Return: Validation status (PASS/REVIEW/FAIL) with confidence and flags
STAGE 3 - ROUTE: Determine: approver based on amount and validation. Rules: <$5K AUTO_APPROVE, $5-50K MANAGER, $50-500K FINANCE_MGR, >$500K CFO. Return: Routing decision with approver assignment
STAGE 4 - OPTIMIZE: Parse: payment terms for discount opportunities. Calculate: ROI for early payment if applicable. Return: Payment recommendation with savings opportunity
STAGE 5 - EXCEPTION: Identify: any issues from previous stages. Create: escalation plan if needed. Return: Exception handling details
FINAL: Return comprehensive JSON with all stage results."""
            logger.info("🤖 Calling orchestrator agent...")
            result = self.orchestrator(prompt)
            logger.info("✅ Orchestrator processing completed")
            return {
                "status": "success",
                "result": result,
                "pdf_path": pdf_path,
                "vendor_name": vendor_name,
                "model_used": self.model
            }
        except Exception as e:
            logger.error(f"❌ Error processing invoice: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "error": str(e),
                "pdf_path": pdf_path,
                "error_type": type(e).__name__
            }

if __name__ == "__main__":
    try:
        orchestrator = InvoiceOrchestrator()
        result = orchestrator.process_invoice("/path/to/sample_invoice.pdf", "Test Vendor")
        logger.info(json.dumps(result, indent=2, default=str))
    except Exception as e:
        logger.error(f"Test failed: {e}", exc_info=True)