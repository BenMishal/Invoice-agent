import google.generativeai as genai
from typing import Dict, Any
import os
import json
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RoutingAgent:
    def __init__(self):
        self.model_name = os.getenv("DEFAULT_MODEL", "gemini-2.0-flash-exp")
        logger.info(f"✅ Initializing Routing Agent")
        genai.configure(***REMOVED***os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel(self.model_name)
        logger.info("✅ Routing Agent created")
    
    def route(self, invoice_data: Dict[str, Any], validation_result: Dict[str, Any]) -> Dict[str, Any]:
        try:
            logger.info(f"🔄 Routing invoice")
            prompt = f"""Route invoice based on: {json.dumps(invoice_data)}
Validation: {json.dumps(validation_result)}
Rules: <$5K AUTO, $5-50K MANAGER, $50-500K FINANCE, >$500K CFO
Return: routing_decision, approver, priority"""
            
            response = self.model.generate_content(prompt)
            return {"status": "success", "routing_decision": response.text}
        except Exception as e:
            logger.error(f"❌ Error: {e}")
            return {"status": "error", "error": str(e)}
