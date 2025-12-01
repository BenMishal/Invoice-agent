import google.generativeai as genai
from typing import Dict, Any, List
import os
import json
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ExceptionHandlerAgent:
    def __init__(self):
        self.model_name = os.getenv("DEFAULT_MODEL", "gemini-2.0-flash-exp")
        logger.info(f"✅ Initializing Exception Handler")
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel(self.model_name)
        logger.info("✅ Exception Handler created")
    
    def handle(self, invoice_data: Dict[str, Any], issues: List[Dict[str, Any]]) -> Dict[str, Any]:
        try:
            logger.info(f"⚠️  Handling exceptions")
            prompt = f"""Handle exceptions for: {json.dumps(invoice_data)}
Issues: {json.dumps(issues)}
Return: exception_type, severity, assigned_to, action_required, escalation_needed"""
            
            response = self.model.generate_content(prompt)
            return {"status": "success", "exception_handling": response.text}
        except Exception as e:
            logger.error(f"❌ Error: {e}")
            return {"status": "error", "error": str(e)}