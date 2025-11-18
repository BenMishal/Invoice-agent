"""Complete system test - API + Agents"""

import requests
import json

BASE_URL = "http://localhost:8080"

def test_root():
    print("\n" + "="*60)
    print("TEST 1: Root Endpoint")
    print("="*60)
    response = requests.get(f"{BASE_URL}/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200
    print("✅ PASSED")

def test_health():
    print("\n" + "="*60)
    print("TEST 2: Health Endpoint")
    print("="*60)
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200
    print("✅ PASSED")

def test_invoice_status():
    print("\n" + "="*60)
    print("TEST 3: Invoice Status Endpoint")
    print("="*60)
    response = requests.get(f"{BASE_URL}/api/v1/invoices/TEST-001/status")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200
    print("✅ PASSED")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("COMPLETE API TEST SUITE")
    print("="*60)
    
    try:
        test_root()
        test_health()
        test_invoice_status()
        
        print("\n" + "="*60)
        print("🎉 ALL TESTS PASSED!")
        print("="*60)
        print("\nYour API is working correctly!")
        print("Next: Test with actual agents")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")

