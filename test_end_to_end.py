from dotenv import load_dotenv
# Load environment variables
load_dotenv()

import os
from agents.orchestrator import InvoiceOrchestrator
from utils.excel_exporter import export_to_excel
import json

def test_invoice_processing():
    print("\n" + "="*60)
    print("END-TO-END INVOICE PROCESSING TEST")
    print("With Handwriting Recognition Support")
    print("="*60)
    
    # Initialize orchestrator
    print("\n1. Initializing orchestrator...")
    orchestrator = InvoiceOrchestrator()
    print("✅ Orchestrator ready")
    
    # Find sample invoices
    invoice_dir = "tests/sample_invoices"
    if not os.path.exists(invoice_dir):
        print(f"\n❌ Directory not found: {invoice_dir}")
        return
    
    # Get all invoice files (PDF, JPG, PNG)
    all_files = os.listdir(invoice_dir)
    pdf_files = [f for f in all_files if f.endswith(('.pdf', '.jpg', '.jpeg', '.png'))]
    
    if not pdf_files:
        print(f"\n❌ No invoice files found in {invoice_dir}")
        return
    
    # Separate handwritten and digital invoices
    handwritten = [f for f in pdf_files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    digital = [f for f in pdf_files if f.lower().endswith('.pdf')]
    
    print(f"\n2. Found {len(pdf_files)} invoice(s) to process")
    print(f"   📄 Digital (PDF): {len(digital)}")
    print(f"   🖊️  Handwritten (Image): {len(handwritten)}")
    
    # Process digital invoices first
    if digital:
        print(f"\n" + "="*60)
        print("PROCESSING DIGITAL INVOICES")
        print("="*60)
        for i, invoice_file in enumerate(digital, 1):
            process_single_invoice(orchestrator, invoice_dir, invoice_file, i, len(digital))
    
    # Process handwritten invoices
    if handwritten:
        print(f"\n" + "="*60)
        print("PROCESSING HANDWRITTEN INVOICES (OCR MODE)")
        print("="*60)
        for i, invoice_file in enumerate(handwritten, 1):
            process_single_invoice(orchestrator, invoice_dir, invoice_file, i, len(handwritten), is_handwritten=True)
    
    print("\n" + "="*60)
    print("END-TO-END TEST COMPLETED")
    print("="*60)
    print("\n✅ Check processed_invoices.xlsx for all extracted data")
    print("✅ Both digital and handwritten invoices processed")

def process_single_invoice(orchestrator, invoice_dir, invoice_file, index, total, is_handwritten=False):
    """Process a single invoice"""
    doc_type = "🖊️ HANDWRITTEN" if is_handwritten else "📄 DIGITAL"
    
    print(f"\n{doc_type} Invoice {index}/{total}: {invoice_file}")
    print("-" * 60)
    
    invoice_path = os.path.join(invoice_dir, invoice_file)
    
    try:
        # Process invoice
        result = orchestrator.process_invoice(
            pdf_path=invoice_path,
            vendor_name="Test Vendor"
        )
        
        print(f"✅ Status: {result['status']}")
        print(f"✅ Document Type: {'Handwritten' if is_handwritten else 'Digital'}")
        
        # Show extracted data preview
        if result['status'] == 'success':
            result_str = str(result.get('result', ''))[:300]
            print(f"\n📊 Preview:")
            print("-" * 60)
            print(result_str)
            if len(str(result.get('result', ''))) > 300:
                print("... (truncated)")
            
            # Export to Excel
            excel_file = export_to_excel(result, "processed_invoices.xlsx")
            if excel_file:
                print(f"\n✅ Exported to Excel: {excel_file}")
        else:
            print(f"⚠️ Extraction incomplete")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_invoice_processing()
