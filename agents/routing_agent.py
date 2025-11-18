from google.adk.agents.llm_agent import Agent
from typing import Dict, Any
import os
import json
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RoutingAgent:
    """Routes validated invoices to appropriate approval workflow"""
    
    def __init__(self):
        self.model = os.getenv("DEFAULT_MODEL", "gemini-2.0-flash-exp")
        logger.info(f"✅ Initializing Routing Agent with model: {self.model}")
        try:
            self.agent = Agent(
                name="routing_agent",
                model=self.model,
                instruction="""You are an invoice routing specialist.
Your task: Determine the optimal approval path for each invoice.

ROUTING RULES - BASED ON AMOUNT AND VALIDATION STATUS:
IF validation_status = PASS:
  - Amount < $5,000: Route to AUTO_APPROVE
  - Amount $5,000-$50,000: Route to DEPARTMENT_MANAGER
  - Amount $50,000-$500,000: Route to FINANCE_MANAGER
  - Amount > $500,000: Route to CFO

IF validation_status = REVIEW:
  - Route to FINANCE_ANALYST for human review

IF validation_status = FAIL:
  - Route to COMPLIANCE_OFFICER for investigation

PRIORITY ASSIGNMENT:
- NORMAL: Amount < $50,000 and PASS validation
- HIGH: Amount $50,000-$500,000 or REVIEW status
- CRITICAL: Amount > $500,000 or FAIL status

RETURN JSON:
{"routing_decision": "AUTO_APPROVE|DEPT_MANAGER|FINANCE_MANAGER|CFO|ANALYST|COMPLIANCE", "approver_role": "string", "approver_email": "string|null", "priority": "NORMAL|HIGH|CRITICAL", "due_date_for_approval": "YYYY-MM-DD", "gl_account_suggested": "string|null", "approval_notes": "string", "escalation_needed": false}"""
            )
            logger.info("✅ Routing Agent created successfully")
        except Exception as e:
            logger.error(f"❌ Error creating routing agent: {str(e)}")
            raise
    
    def route(self, invoice_data: Dict[str, Any], validation_result: Dict[str, Any]) -> Dict[str, Any]:
        """Route invoice to appropriate approver"""
        try:
            invoice_num = invoice_data.get('invoice_number', 'unknown')
            logger.info(f"🔄 Routing invoice: {invoice_num}")
            prompt = f"""Route this invoice based on validation status and amount:
INVOICE DATA:
{json.dumps(invoice_data, indent=2)}
VALIDATION RESULT:
{json.dumps(validation_result, indent=2)}
Apply the routing rules and return the JSON decision."""
            logger.info("🤖 Calling routing agent...")
            result = self.agent(prompt)
            logger.info("✅ Routing completed")
            routing_json = result
            if isinstance(result, str):
                try:
                    routing_json = json.loads(result)
                    decision = routing_json.get('routing_decision', 'UNKNOWN')
                    logger.info(f"✅ Routing decision: {decision}")
                except json.JSONDecodeError:
                    routing_json = {"routing_decision": "ANALYST", "raw_result": result}
                    logger.warning("⚠️  Could not parse routing result")
            return {
                "status": "success",
                "routing_decision": routing_json,
                "invoice_number": invoice_num,
                "model_used": self.model
            }
        except Exception as e:
            logger.error(f"❌ Error routing invoice: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "error": str(e),
                "invoice_number": invoice_data.get('invoice_number'),
                "error_type": type(e).__name__
            }

if __name__ == "__main__":
    try:
        router = RoutingAgent()
        sample_invoice = {"invoice_number": "INV-2025-001", "amount_total": 35000.00}
        sample_validation = {"status": "PASS"}
        result = router.route(sample_invoice, sample_validation)
        logger.info(json.dumps(result, indent=2, default=str))
    except Exception as e:
        logger.error(f"Test failed: {e}", exc_info=True)