"""Advanced handwriting recognition test"""
import os
from agents.capture_agent import CaptureAgent
import json

def test_handwriting_recognition():
    print("\n" + "="*60)
    print("ADVANCED HANDWRITING RECOGNITION TEST")
    print("="*60)
    
    # Initialize capture agent
    print("\n1. Initializing Capture Agent...")
    capture = CaptureAgent(model_name="gemini-2.0-flash")
    print("✅ Capture Agent ready")
    
    # Find handwritten invoices
    invoice_dir = "tests/sample_invoices"
    handwritten_files = [
        f for f in os.listdir(invoice_dir)
        if f.lower().endswith(('.jpg', '.jpeg', '.png'))
    ]
    
    if not handwritten_files:
        print(f"\n❌ No handwritten invoices found in {invoice_dir}")
        print("Please add JPG/PNG images of handwritten invoices")
        return
    
    print(f"\n2. Found {len(handwritten_files)} handwritten invoice(s)")
    
    # Process each handwritten invoice
    for i, filename in enumerate(handwritten_files, 1):
        print(f"\n" + "="*60)
        print(f"Processing Handwritten Invoice {i}/{len(handwritten_files)}")
        print(f"File: {filename}")
        print("="*60)
        
        file_path = os.path.join(invoice_dir, filename)
        
        try:
            # Extract from handwritten invoice
            result = capture.extract_from_handwritten_invoice(file_path)
            
            print(f"\n✅ Status: {result['status']}")
            print(f"✅ Document Type: {result['document_type']}")
            print(f"✅ Confidence: {result.get('confidence', 'unknown')}")
            
            if result['status'] == 'success':
                extracted_data = result['extracted_data']
                print(f"\n📊 Extracted Data (Preview):")
                print("-" * 60)
                print(extracted_data[:500])
                if len(extracted_data) > 500:
                    print("... (truncated)")
                
                # Try to parse as JSON to show structured data
                try:
                    data = json.loads(extracted_data)
                    print(f"\n📋 Structured Extraction:")
                    print(f"  Invoice Number: {data.get('invoice_number', 'N/A')}")
                    print(f"  Vendor Name: {data.get('vendor_name', 'N/A')}")
                    print(f"  Date: {data.get('invoice_date', 'N/A')}")
                    print(f"  Amount: {data.get('total_amount', 'N/A')}")
                    print(f"  Extraction Notes: {data.get('notes', 'N/A')}")
                except json.JSONDecodeError:
                    print("⚠️ Could not parse as JSON (checking raw extraction...)")
            else:
                print(f"❌ Error: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
    
    print("\n" + "="*60)
    print("HANDWRITING TEST COMPLETED")
    print("="*60)

if __name__ == "__main__":
    test_handwriting_recognition()
