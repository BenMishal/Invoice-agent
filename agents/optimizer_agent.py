from google.adk.agents.llm_agent import Agent
from typing import Dict, Any
import os
import json
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OptimizationAgent:
    """Analyzes payment opportunities and optimal payment timing"""
    
    def __init__(self):
        self.model = os.getenv("DEFAULT_MODEL", "gemini-2.0-flash-exp")
        logger.info(f"✅ Initializing Optimization Agent with model: {self.model}")
        try:
            self.agent = Agent(
                name="payment_optimizer_agent",
                model=self.model,
                instruction="""You are a financial optimization specialist.
Your task: Optimize payment timing to maximize discounts and cash flow.

PAYMENT OPTIMIZATION ANALYSIS:
1. PARSE PAYMENT TERMS - Extract discount info from "2/10 Net 30" format
2. CALCULATE DISCOUNT VALUE - discount_amount = invoice_total × discount_percent
3. CALCULATE ROI - (discount_percent / days_saved) × 365. If ROI > 10%: recommend early payment
4. CASH FLOW - Can company afford early payment?
5. RECOMMENDATION - If ROI > 10%: pay early. If ROI < 10%: pay on due date

RETURN JSON:
{"payment_terms_parsed": "string", "discount_available": true|false, "discount_percent": 0.02, "discount_days": 10, "discount_amount": 2000.0, "early_payment_date": "YYYY-MM-DD|null", "full_payment_date": "YYYY-MM-DD", "recommended_payment_date": "YYYY-MM-DD", "annualized_roi_percent": 36.5, "cash_impact": "POSITIVE|NEUTRAL|NEGATIVE", "recommendation": "Pay early for discount|Pay on due date", "savings_opportunity": 2000.0}"""
            )
            logger.info("✅ Optimization Agent created successfully")
        except Exception as e:
            logger.error(f"❌ Error creating optimization agent: {str(e)}")
            raise
    
    def optimize(self, invoice_data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize payment timing for invoice"""
        try:
            invoice_num = invoice_data.get('invoice_number', 'unknown')
            logger.info(f"💰 Optimizing payment for: {invoice_num}")
            prompt = f"""Optimize the payment strategy for this invoice:
{json.dumps(invoice_data, indent=2)}
Analyze payment terms, calculate discount ROI, and recommend optimal payment date."""
            logger.info("🤖 Calling optimization agent...")
            result = self.agent(prompt)
            logger.info("✅ Payment optimization completed")
            optimization_json = result
            if isinstance(result, str):
                try:
                    optimization_json = json.loads(result)
                    savings = optimization_json.get('savings_opportunity', 0)
                    if savings > 0:
                        logger.info(f"✅ Potential savings: ${savings}")
                except json.JSONDecodeError:
                    optimization_json = {"recommendation": "Pay on due date", "raw_result": result}
                    logger.warning("⚠️  Could not parse optimization result")
            return {
                "status": "success",
                "payment_optimization": optimization_json,
                "invoice_number": invoice_num,
                "model_used": self.model
            }
        except Exception as e:
            logger.error(f"❌ Error optimizing payment: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "error": str(e),
                "invoice_number": invoice_data.get('invoice_number'),
                "error_type": type(e).__name__
            }

if __name__ == "__main__":
    try:
        optimizer = OptimizationAgent()
        sample_invoice = {
            "invoice_number": "INV-2025-001",
            "amount_total": 100000.00,
            "payment_terms": "2/10 Net 30",
            "due_date": "2025-12-17"
        }
        result = optimizer.optimize(sample_invoice)
        logger.info(json.dumps(result, indent=2, default=str))
    except Exception as e:
        logger.error(f"Test failed: {e}", exc_info=True)