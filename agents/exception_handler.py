from google.adk.agents.llm_agent import Agent
from typing import Dict, Any, List
import os
import json
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ExceptionHandlerAgent:
    """Handles invoice processing exceptions and creates escalations"""
    
    def __init__(self):
        self.model = os.getenv("DEFAULT_MODEL", "gemini-2.0-flash-exp")
        logger.info(f"✅ Initializing Exception Handler with model: {self.model}")
        try:
            self.agent = Agent(
                name="exception_handler_agent",
                model=self.model,
                instruction="""You are an exception management specialist.
Your task: Handle invoice exceptions and create appropriate escalations.

EXCEPTION TYPES:
1. DUPLICATE - Same invoice twice. Assign to: AP MANAGER. Priority: MEDIUM
2. FRAUD_SIGNAL - High-risk patterns. Assign to: COMPLIANCE OFFICER. Priority: CRITICAL
3. VALIDATION_FAIL - Data quality issues. Assign to: FINANCE ANALYST. Priority: HIGH
4. MISSING_PO - No Purchase Order found. Assign to: PROCUREMENT MANAGER. Priority: MEDIUM
5. VENDOR_NEW - Unvetted vendor. Assign to: VENDOR MANAGER. Priority: LOW
6. CALCULATION_ERROR - Numbers mismatch. Assign to: FINANCE ANALYST. Priority: MEDIUM
7. MISSING_REQUIRED_DATA - Critical fields missing. Assign to: AP COORDINATOR. Priority: LOW
8. HIGH_AMOUNT - Unusual amount. Assign to: FINANCE MANAGER. Priority: HIGH

FOR EACH EXCEPTION:
- exception_type: From list above
- severity: LOW|MEDIUM|HIGH|CRITICAL
- assigned_to: Role/department
- priority: LOW|MEDIUM|HIGH|CRITICAL
- action_required: What to do
- escalation_needed: true|false
- next_steps: Array of action steps
- estimated_resolution_time: Time estimate
- notification_required: Send notification?

RETURN JSON:
{"exception_type": "string", "severity": "LOW|MEDIUM|HIGH|CRITICAL", "assigned_to": "string", "priority": "LOW|MEDIUM|HIGH|CRITICAL", "action_required": "string", "escalation_needed": false, "next_steps": [], "estimated_resolution_time": "string", "notification_required": true}"""
            )
            logger.info("✅ Exception Handler created successfully")
        except Exception as e:
            logger.error(f"❌ Error creating exception handler: {str(e)}")
            raise
    
    def handle(self, invoice_data: Dict[str, Any], issues: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Handle invoice exceptions"""
        try:
            invoice_num = invoice_data.get('invoice_number', 'unknown')
            logger.info(f"⚠️  Handling exceptions for: {invoice_num}")
            logger.info(f"   Issues count: {len(issues)}")
            prompt = f"""Handle these exceptions for the invoice:
INVOICE DATA:
{json.dumps(invoice_data, indent=2)}
ISSUES FOUND ({len(issues)} total):
{json.dumps(issues, indent=2)}
For each issue, analyze it and create an exception handling plan.
Return JSON with exception details and escalation strategy."""
            logger.info("🤖 Calling exception handler agent...")
            result = self.agent(prompt)
            logger.info("✅ Exception handling completed")
            exception_json = result
            if isinstance(result, str):
                try:
                    exception_json = json.loads(result)
                    exc_type = exception_json.get('exception_type', 'UNKNOWN')
                    logger.info(f"✅ Exception type: {exc_type}")
                except json.JSONDecodeError:
                    exception_json = {"exception_type": "UNKNOWN", "raw_result": result}
                    logger.warning("⚠️  Could not parse exception handling result")
            return {
                "status": "success",
                "exception_handling": exception_json,
                "invoice_number": invoice_num,
                "issues_count": len(issues),
                "model_used": self.model
            }
        except Exception as e:
            logger.error(f"❌ Error handling exceptions: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "error": str(e),
                "invoice_number": invoice_data.get('invoice_number'),
                "error_type": type(e).__name__
            }

if __name__ == "__main__":
    try:
        handler = ExceptionHandlerAgent()
        sample_invoice = {
            "invoice_number": "INV-2025-001",
            "vendor_name": "Unknown Vendor",
            "amount_total": 250000.00
        }
        sample_issues = [
            {"type": "NEW_VENDOR", "severity": "MEDIUM"},
            {"type": "HIGH_AMOUNT", "severity": "HIGH"}
        ]
        result = handler.handle(sample_invoice, sample_issues)
        logger.info(json.dumps(result, indent=2, default=str))
    except Exception as e:
        logger.error(f"Test failed: {e}", exc_info=True)