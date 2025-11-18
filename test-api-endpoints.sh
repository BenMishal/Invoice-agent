#!/bin/bash
# ============================================================================
# TEST ALL ENDPOINTS - Quick API Test
# Save as: test-api.sh
# Usage: ./test-api.sh
# ============================================================================

echo "================================"
echo "Testing Invoice Processing API"
echo "================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if API is running
if ! curl -s http://localhost:8080/health > /dev/null; then
    echo -e "${RED}❌ API is not running!${NC}"
    echo "Start it first: ./start-api.sh"
    exit 1
fi

echo -e "${GREEN}✅ API is running${NC}"
echo ""

# Test 1: Root endpoint
echo "Test 1: Root Endpoint"
echo "======================"
curl -s http://localhost:8080/ | python -m json.tool
echo ""
echo ""

# Test 2: Health endpoint
echo "Test 2: Health Endpoint"
echo "======================="
curl -s http://localhost:8080/health | python -m json.tool
echo ""
echo ""

# Test 3: Invoice status
echo "Test 3: Invoice Status"
echo "======================"
curl -s http://localhost:8080/api/v1/invoices/TEST-001/status | python -m json.tool
echo ""
echo ""

# Summary
echo "================================"
echo "All endpoint tests completed!"
echo "================================"
echo ""
echo "Next steps:"
echo "1. Visit http://localhost:8080/docs for interactive docs"
echo "2. Test with actual PDF: curl -X POST http://localhost:8080/api/v1/invoices/process -F 'file=@invoice.pdf'"
echo ""
