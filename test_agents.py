"""Test all agents individually"""
import json
from agents.orchestrator import InvoiceOrchestrator
from agents.capture_agent import InvoiceCaptureAgent
from agents.validation_agent import ValidationAgent
from agents.routing_agent import RoutingAgent
from agents.optimizer_agent import OptimizationAgent
from agents.exception_handler import ExceptionHandlerAgent

def test_orchestrator():
    print("\n" + "="*60)
    print("TEST 1: Orchestrator Agent")
    print("="*60)
    try:
        orchestrator = InvoiceOrchestrator()
        print("✅ Orchestrator initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Orchestrator failed: {e}")
        return False

def test_capture():
    print("\n" + "="*60)
    print("TEST 2: Capture Agent")
    print("="*60)
    try:
        capture = InvoiceCaptureAgent()
        print("✅ Capture agent initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Capture agent failed: {e}")
        return False

def test_validation():
    print("\n" + "="*60)
    print("TEST 3: Validation Agent")
    print("="*60)
    try:
        validator = ValidationAgent()
        print("✅ Validation agent initialized successfully")
        
        sample_data = {
            "invoice_number": "TEST-001",
            "vendor_name": "Test Vendor",
            "invoice_date": "2025-11-18",
            "due_date": "2025-12-18",
            "amount_total": 5000.00,
            "currency": "USD",
            "tax_amount": 500.00,
            "payment_terms": "Net 30"
        }
        
        result = validator.validate(sample_data)
        print(f"✅ Validation completed: {result['status']}")
        return True
    except Exception as e:
        print(f"❌ Validation agent failed: {e}")
        return False

def test_routing():
    print("\n" + "="*60)
    print("TEST 4: Routing Agent")
    print("="*60)
    try:
        router = RoutingAgent()
        print("✅ Routing agent initialized successfully")
        
        sample_invoice = {"invoice_number": "TEST-001", "amount_total": 35000.00}
        sample_validation = {"status": "PASS"}
        
        result = router.route(sample_invoice, sample_validation)
        print(f"✅ Routing completed: {result['status']}")
        return True
    except Exception as e:
        print(f"❌ Routing agent failed: {e}")
        return False

def test_optimizer():
    print("\n" + "="*60)
    print("TEST 5: Optimizer Agent")
    print("="*60)
    try:
        optimizer = OptimizationAgent()
        print("✅ Optimizer agent initialized successfully")
        
        sample_invoice = {
            "invoice_number": "TEST-001",
            "amount_total": 100000.00,
            "payment_terms": "2/10 Net 30",
            "due_date": "2025-12-18"
        }
        
        result = optimizer.optimize(sample_invoice)
        print(f"✅ Optimization completed: {result['status']}")
        return True
    except Exception as e:
        print(f"❌ Optimizer agent failed: {e}")
        return False

def test_exception_handler():
    print("\n" + "="*60)
    print("TEST 6: Exception Handler Agent")
    print("="*60)
    try:
        handler = ExceptionHandlerAgent()
        print("✅ Exception handler initialized successfully")
        
        sample_invoice = {
            "invoice_number": "TEST-001",
            "vendor_name": "Unknown Vendor",
            "amount_total": 250000.00
        }
        sample_issues = [
            {"type": "NEW_VENDOR", "severity": "MEDIUM"},
            {"type": "HIGH_AMOUNT", "severity": "HIGH"}
        ]
        
        result = handler.handle(sample_invoice, sample_issues)
        print(f"✅ Exception handling completed: {result['status']}")
        return True
    except Exception as e:
        print(f"❌ Exception handler failed: {e}")
        return False

if __name__ == "__main__":
    print("\n" + "="*60)
    print("TESTING ALL AGENTS")
    print("="*60)
    
    results = []
    results.append(("Orchestrator", test_orchestrator()))
    results.append(("Capture", test_capture()))
    results.append(("Validation", test_validation()))
    results.append(("Routing", test_routing()))
    results.append(("Optimizer", test_optimizer()))
    results.append(("Exception Handler", test_exception_handler()))
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print("\n" + "="*60)
    print(f"TOTAL: {passed}/{total} tests passed")
    print("="*60)
    
    if passed == total:
        print("\n🎉 All agents working correctly!")
        print("Next: Create sample invoices and test end-to-end")
    else:
        print(f"\n⚠️  {total - passed} agent(s) need attention")
