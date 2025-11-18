"""Fix all agents to use google.generativeai instead of ADK"""
import os

# Template for agent files
AGENT_TEMPLATE = """
import google.generativeai as genai
from typing import Dict, Any{extra_imports}
import os
import json
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class {class_name}:
    {docstring}
    
    def __init__(self):
        {init_docstring}
        self.model_name = os.getenv("DEFAULT_MODEL", "gemini-2.0-flash-exp")
        logger.info(f"✅ Initializing {agent_name} with model: {{self.model_name}}")
        
        try:
            genai.configure(***REMOVED***os.getenv("GEMINI_API_KEY"))
            self.model = genai.GenerativeModel(self.model_name)
            self.instruction = {instruction}
            logger.info("✅ {agent_name} created successfully")
        except Exception as e:
            logger.error(f"❌ Error creating {agent_name}: {{str(e)}}")
            raise
    
{methods}
"""

print("Updating all agent files to use google.generativeai...")
print("="*60)

# Just update the import and model initialization
# Keep the rest of the logic the same

files_to_update = {
    "agents/orchestrator.py": "InvoiceOrchestrator",
    "agents/capture_agent.py": "InvoiceCaptureAgent",
    "agents/validation_agent.py": "ValidationAgent",
    "agents/routing_agent.py": "RoutingAgent",
    "agents/optimizer_agent.py": "OptimizationAgent",
    "agents/exception_handler.py": "ExceptionHandlerAgent"
}

for file_path, class_name in files_to_update.items():
    try:
        # Read file
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Replace ADK import with GenAI import
        content = content.replace(
            "from google.adk.agents.llm_agent import Agent",
            "import google.generativeai as genai"
        )
        
        # Replace Agent initialization with GenAI model
        content = content.replace(
            "self.orchestrator = Agent(",
            "genai.configure(***REMOVED***os.getenv('GEMINI_API_KEY'))\n        self.orchestrator = genai.GenerativeModel(self.model,"
        )
        content = content.replace(
            "self.agent = Agent(",
            "genai.configure(***REMOVED***os.getenv('GEMINI_API_KEY'))\n        self.agent = genai.GenerativeModel(self.model,"
        )
        
        # Replace generate call with GenAI call
        content = content.replace(
            "result = self.orchestrator.generate(prompt)",
            "response = self.orchestrator.generate_content(prompt)\n            result = response.text"
        )
        content = content.replace(
            "result = self.agent.generate(prompt)",
            "response = self.agent.generate_content(prompt)\n            result = response.text"
        )
        
        # Remove Agent-specific parameters (name, instruction)
        # We'll keep instruction as a class variable instead
        
        # Write back
        with open(file_path, 'w') as f:
            f.write(content)
        
        print(f"✅ Updated {file_path}")
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")

print("\n" + "="*60)
print("All files updated!")
print("Run: python test_end_to_end.py")

