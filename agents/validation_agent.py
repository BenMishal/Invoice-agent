import google.generativeai as genai
from typing import Dict, Any
import os
import json
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ValidationAgent:
    def __init__(self):
        self.model_name = os.getenv("DEFAULT_MODEL", "gemini-2.0-flash-exp")
        logger.info(f"✅ Initializing Validation Agent")
        genai.configure(***REMOVED***os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel(self.model_name)
        logger.info("✅ Validation Agent created")
    
    def validate(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            logger.info(f"✅ Validating invoice")
            prompt = f"""Validate this invoice data: {json.dumps(extracted_data)}
Check: completeness, format, calculations, duplicates, fraud signals
Return: status (PASS/REVIEW/FAIL), confidence, flags"""
            
            response = self.model.generate_content(prompt)
            return {"status": "success", "validation_result": response.text}
        except Exception as e:
            logger.error(f"❌ Error: {e}")
            return {"status": "error", "error": str(e)}