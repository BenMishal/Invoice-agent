#!/bin/bash
echo "Fixing all agent files..."

# Fix orchestrator.py
sed -i.bak 's/result = self\.orchestrator(prompt)/result = self.orchestrator.generate(prompt)/g' agents/orchestrator.py
echo "✅ Fixed orchestrator.py"

# Fix capture_agent.py
sed -i.bak 's/result = self\.agent(prompt)/result = self.agent.generate(prompt)/g' agents/capture_agent.py
echo "✅ Fixed capture_agent.py"

# Fix validation_agent.py
sed -i.bak 's/result = self\.agent(prompt)/result = self.agent.generate(prompt)/g' agents/validation_agent.py
echo "✅ Fixed validation_agent.py"

# Fix routing_agent.py
sed -i.bak 's/result = self\.agent(prompt)/result = self.agent.generate(prompt)/g' agents/routing_agent.py
echo "✅ Fixed routing_agent.py"

# Fix optimizer_agent.py
sed -i.bak 's/result = self\.agent(prompt)/result = self.agent.generate(prompt)/g' agents/optimizer_agent.py
echo "✅ Fixed optimizer_agent.py"

# Fix exception_handler.py
sed -i.bak 's/result = self\.agent(prompt)/result = self.agent.generate(prompt)/g' agents/exception_handler.py
echo "✅ Fixed exception_handler.py"

echo ""
echo "All files fixed! Backup files saved with .bak extension"
echo "Run: python test_end_to_end.py to test again"
