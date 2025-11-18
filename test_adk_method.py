"""Test which method works for google-adk"""
from google.adk.agents.llm_agent import Agent
import os
from dotenv import load_dotenv

load_dotenv()

# Create test agent
agent = Agent(
    name="test_agent",
    model=os.getenv("DEFAULT_MODEL", "gemini-2.0-flash-exp"),
    instruction="You are a test agent. Respond with 'Hello World'"
)

print("Testing different methods to call the agent...")
print("="*60)

# Method 1: Direct call
print("\n1. Testing: agent(prompt)")
try:
    result = agent("Say hello")
    print("✅ SUCCESS - Use: agent(prompt)")
    print(f"Result: {result}")
except Exception as e:
    print(f"❌ FAILED: {e}")

# Method 2: .generate()
print("\n2. Testing: agent.generate(prompt)")
try:
    result = agent.generate("Say hello")
    print("✅ SUCCESS - Use: agent.generate(prompt)")
    print(f"Result: {result}")
except Exception as e:
    print(f"❌ FAILED: {e}")

# Method 3: .run()
print("\n3. Testing: agent.run(prompt)")
try:
    result = agent.run("Say hello")
    print("✅ SUCCESS - Use: agent.run(prompt)")
    print(f"Result: {result}")
except Exception as e:
    print(f"❌ FAILED: {e}")

# Method 4: .execute()
print("\n4. Testing: agent.execute(prompt)")
try:
    result = agent.execute("Say hello")
    print("✅ SUCCESS - Use: agent.execute(prompt)")
    print(f"Result: {result}")
except Exception as e:
    print(f"❌ FAILED: {e}")

# Method 5: Check available methods
print("\n5. Available methods on agent:")
print("="*60)
methods = [m for m in dir(agent) if not m.startswith('_')]
for method in methods:
    print(f"  - {method}")

print("\n" + "="*60)
print("Use the method that showed ✅ SUCCESS above")

