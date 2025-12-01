import google.generativeai as genai
from typing import Dict, Any
import os
import json
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OptimizationAgent:
    def __init__(self):
        self.model_name = os.getenv("DEFAULT_MODEL", "gemini-2.0-flash-exp")
        logger.info(f"✅ Initializing Optimization Agent")
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel(self.model_name)
        logger.info("✅ Optimization Agent created")
    
    def optimize(self, invoice_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            logger.info(f"💰 Optimizing payment")
            prompt = f"""Optimize payment for: {json.dumps(invoice_data)}
Parse payment terms, calculate discount ROI, recommend optimal payment date
Return: discount_available, savings_opportunity, recommended_payment_date"""
            
            response = self.model.generate_content(prompt)
            return {"status": "success", "payment_optimization": response.text}
        except Exception as e:
            logger.error(f"❌ Error: {e}")
            return {"status": "error", "error": str(e)}