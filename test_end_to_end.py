"""End-to-end test with sample invoices"""
import os
from agents.orchestrator import InvoiceOrchestrator
from utils.excel_exporter import export_to_excel

def test_invoice_processing():
    print("\n" + "="*60)
    print("END-TO-END INVOICE PROCESSING TEST")
    print("="*60)
    
    # Initialize orchestrator
    print("\n1. Initializing orchestrator...")
    orchestrator = InvoiceOrchestrator()
    print("✅ Orchestrator ready")
    
    # Find sample invoices
    invoice_dir = "/Users/benmishal/Desktop/Invoice-agent/Invoice-agent/tests/sample_invoices/"
    if not os.path.exists(invoice_dir):
        print(f"\n❌ Directory not found: {invoice_dir}")
        print("Please create sample invoices first")
        return
    
    pdf_files = [f for f in os.listdir(invoice_dir) if f.endswith('.pdf')]
    
    if not pdf_files:
        print(f"\n❌ No PDF files found in {invoice_dir}")
        print("Please add sample invoice PDFs")
        return
    
    print(f"\n2. Found {len(pdf_files)} invoice(s) to process")
    
    # Process each invoice
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"\n" + "="*60)
        print(f"Processing Invoice {i}/{len(pdf_files)}: {pdf_file}")
        print("="*60)
        
        pdf_path = os.path.join(invoice_dir, pdf_file)
        
        try:
            # Process invoice
            result = orchestrator.process_invoice(
                pdf_path=pdf_path,
                vendor_name="Test Vendor"
            )
            
            print(f"\n✅ Status: {result['status']}")
            print(f"✅ Model: {result.get('model_used', 'unknown')}")
            
            # Show result preview
            if result['status'] == 'success':
                print("\n📊 Processing Result:")
                print("-" * 60)
                result_str = str(result.get('result', ''))[:500]
                print(result_str)
                if len(str(result.get('result', ''))) > 500:
                    print("... (truncated)")

        except Exception as e:
            print(f"\n❌ Error processing {pdf_file}:")
            print(f"   {str(e)}")
    
     # Export to Excel
        excel_file = export_to_excel(result, "processed_invoices.xlsx")
        if excel_file:
            print(f"\n📊 Exported to Excel: {excel_file}")
            print("\n" + "="*60)
            print("END-TO-END TEST COMPLETED")
            print("="*60)

if __name__ == "__main__":
    test_invoice_processing()

