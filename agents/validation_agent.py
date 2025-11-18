from google.adk.agents.llm_agent import Agent
from typing import Dict, Any
import os
import json
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ValidationAgent:
    """Validates invoice data and detects duplicates/fraud signals"""
    
    def __init__(self):
        self.model = os.getenv("DEFAULT_MODEL", "gemini-2.0-flash-exp")
        logger.info(f"✅ Initializing Validation Agent with model: {self.model}")
        try:
            self.agent = Agent(
                name="validation_agent",
                model=self.model,
                instruction="""You are an invoice validation and fraud detection specialist.
Your task: Validate invoice data and identify any issues.

PERFORM THESE 5 CHECKS:
1. DATA COMPLETENESS - Are all required fields present? Check: invoice_number, vendor_name, invoice_date, due_date, amount_total, currency
2. DATA FORMAT - Are dates YYYY-MM-DD? Are amounts numbers? Is currency valid ISO code?
3. CALCULATION ACCURACY - Do line items sum to subtotal? Does subtotal + tax = total?
4. DUPLICATE DETECTION - Same vendor + similar amount (±10%) + recent date (±7 days)?
5. FRAUD SIGNALS - Check: HIGH_AMOUNT (>$100K), NEW_VENDOR, UNUSUAL_TERMS, EMAIL_MISMATCH

OVERALL STATUS:
- PASS: All checks pass, no flags
- REVIEW: Checks pass but has flags, requires human review
- FAIL: Any critical check fails

RETURN JSON:
{"status": "PASS|REVIEW|FAIL", "overall_confidence": 0.0-1.0, "checks": {"completeness": "PASS|FAIL", "format": "PASS|FAIL", "calculations": "PASS|FAIL", "duplicates": "PASS|FAIL", "fraud_signals": "PASS|FLAG"}, "flags": [{"type": "HIGH_AMOUNT|NEW_VENDOR|UNUSUAL_TERMS|EMAIL_MISMATCH|DUPLICATE", "severity": "LOW|MEDIUM|HIGH", "description": "string"}], "issues": [], "recommendation": "Approve|Review|Reject", "human_review_required": false}"""
            )
            logger.info("✅ Validation Agent created successfully")
        except Exception as e:
            logger.error(f"❌ Error creating validation agent: {str(e)}")
            raise
    
    def validate(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate extracted invoice data"""
        try:
            invoice_num = extracted_data.get('invoice_number', 'unknown')
            logger.info(f"✅ Validating invoice: {invoice_num}")
            prompt = f"""Validate this invoice data:
{json.dumps(extracted_data, indent=2)}
Perform all 5 validation checks and return the JSON result."""
            logger.info("🤖 Calling validation agent...")
            result = self.agent(prompt)
            logger.info("✅ Validation completed")
            validation_json = result
            if isinstance(result, str):
                try:
                    validation_json = json.loads(result)
                    logger.info(f"✅ Validation status: {validation_json.get('status')}")
                except json.JSONDecodeError:
                    validation_json = {"status": "REVIEW", "raw_result": result}
                    logger.warning("⚠️  Could not parse validation result")
            return {
                "status": "success",
                "validation_result": validation_json,
                "invoice_number": invoice_num,
                "model_used": self.model
            }
        except Exception as e:
            logger.error(f"❌ Error validating invoice: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "error": str(e),
                "invoice_number": extracted_data.get('invoice_number'),
                "error_type": type(e).__name__
            }

if __name__ == "__main__":
    try:
        validator = ValidationAgent()
        sample_data = {
            "invoice_number": "INV-2025-001",
            "vendor_name": "Test Vendor",
            "invoice_date": "2025-11-17",
            "due_date": "2025-12-17",
            "amount_total": 5000.00,
            "currency": "USD",
            "tax_amount": 500.00,
            "payment_terms": "Net 30"
        }
        result = validator.validate(sample_data)
        logger.info(json.dumps(result, indent=2, default=str))
    except Exception as e:
        logger.error(f"Test failed: {e}", exc_info=True)
