"""Test handwritten invoice processing"""
import os
from agents.capture_agent import InvoiceCaptureAgent
import json

def test_handwritten():
    print("\n" + "="*60)
    print("HANDWRITTEN INVOICE TEST")
    print("="*60)
    
    # Initialize agent
    agent = InvoiceCaptureAgent()
    
    # Check for handwritten test images
    test_dir = "tests/sample_invoices"
    handwritten_files = [f for f in os.listdir(test_dir) 
                         if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    if not handwritten_files:
        print("\n⚠️  No handwritten invoice images found")
        print("Please add a handwritten invoice image to:")
        print(f"   {test_dir}/")
        print("\nSupported formats: .jpg, .jpeg, .png")
        print("\nHow to create test image:")
        print("1. Write a simple invoice by hand")
        print("2. Take a photo with your phone")
        print("3. Transfer to: tests/sample_invoices/")
        return
    
    print(f"\n✅ Found {len(handwritten_files)} handwritten test file(s)")
    
    for img_file in handwritten_files:
        img_path = os.path.join(test_dir, img_file)
        
        print(f"\n" + "-"*60)
        print(f"Testing: {img_file}")
        print("-"*60)
        
        # Extract handwritten data
        result = agent.extract_handwritten(img_path)
        
        print(f"\nStatus: {result['status']}")
        if result['status'] == 'success':
            print(f"Source Type: {result['source_type']}")
            print(f"\nExtracted Data:")
            print(result['extracted_data'][:500])  # Show first 500 chars
        else:
            print(f"Error: {result.get('error')}")
    
    print("\n" + "="*60)
    print("TEST COMPLETE")
    print("="*60)

if __name__ == "__main__":
    test_handwritten()

