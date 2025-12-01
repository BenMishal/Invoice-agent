"""Excel export utilities for processed invoices"""
import pandas as pd
import json
import re
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def clean_extracted_data(data: dict) -> dict:
    """Clean extracted data by removing placeholder values"""
    cleaned = {}
    
    placeholder_values = [
        'Not Found', 'Not found', 'TBD', 'To be extracted', 'To be determined',
        'YYYY-MM-DD', 'yyyy-mm-dd', 'DD-MM-YYYY', 'mm/dd/yyyy',
        'INVOICE_NUMBER_EXTRACTED', 'INVOICE_DATE_EXTRACTED', 'CURRENCY_EXTRACTED',
        'TOTAL_AMOUNT_EXTRACTED', 'PAYMENT_TERMS_EXTRACTED',
        'To be determined by OCR/extraction',
        'TBD - to be extracted', 'pending', 'null', 'None'
    ]
    
    for key, value in data.items():
        if not value:
            cleaned[key] = ''
        elif isinstance(value, str):
            # Check if it's a placeholder
            if any(placeholder.lower() in str(value).lower() for placeholder in placeholder_values):
                cleaned[key] = ''
            else:
                cleaned[key] = value.strip()
        elif isinstance(value, (int, float)):
            cleaned[key] = value if value != 0 else ''
        else:
            cleaned[key] = value
    
    return cleaned

def extract_invoice_data_from_json(json_str: str) -> dict:
    """Extract invoice data from various JSON structures"""
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError:
        logger.warning(f"JSON decode error, attempting fallback extraction")
        return extract_with_regex(json_str)
    
    # Initialize result
    result = {
        'vendor_name': '',
        'invoice_number': '',
        'invoice_date': '',
        'due_date': '',
        'total_amount': '',
        'tax_amount': '',
        'currency': '',
        'payment_terms': ''
    }
    
    # Handle different JSON structures returned by different Gemini prompts
    
    # Structure 1: Direct fields at top level
    if 'invoice_number' in data:
        result['invoice_number'] = data.get('invoice_number', '')
    
    # Structure 2: Nested under 'extracted_data'
    if 'extracted_data' in data:
        extracted = data['extracted_data']
        result.update({
            'vendor_name': extracted.get('vendor_name', '') or extracted.get('vendor', ''),
            'invoice_number': extracted.get('invoice_number', ''),
            'invoice_date': extracted.get('invoice_date', ''),
            'due_date': extracted.get('due_date', ''),
            'total_amount': extracted.get('total_amount', extracted.get('amount', '')),
            'tax_amount': extracted.get('tax', extracted.get('tax_amount', '')),
            'currency': extracted.get('currency', 'USD'),
            'payment_terms': extracted.get('payment_terms', '')
        })
    
    # Structure 3: Nested under 'data' or 'details'
    elif 'data' in data:
        data_section = data['data']
        result.update({
            'vendor_name': data_section.get('vendor_name', '') or data_section.get('vendor', ''),
            'invoice_number': data_section.get('invoice_number', ''),
            'invoice_date': data_section.get('invoice_date', ''),
            'due_date': data_section.get('due_date', ''),
            'total_amount': data_section.get('total_amount', data_section.get('amount', '')),
            'tax_amount': data_section.get('tax', ''),
            'currency': data_section.get('currency', 'USD'),
            'payment_terms': data_section.get('payment_terms', '')
        })
    
    # Structure 4: Nested under stages -> capture
    elif 'stages' in data and 'capture' in data['stages']:
        capture = data['stages']['capture'].get('extracted_data', {})
        result.update({
            'vendor_name': capture.get('vendor_name', '') or capture.get('vendor', ''),
            'invoice_number': capture.get('invoice_number', ''),
            'invoice_date': capture.get('invoice_date', ''),
            'due_date': capture.get('due_date', ''),
            'total_amount': capture.get('total_amount', capture.get('amount', '')),
            'tax_amount': capture.get('tax', ''),
            'currency': capture.get('currency', 'USD'),
            'payment_terms': capture.get('payment_terms', '')
        })
    
    # Fallback: Try to extract from any top-level fields
    else:
        result.update({
            'vendor_name': data.get('vendor_name', '') or data.get('vendor', ''),
            'invoice_number': data.get('invoice_number', ''),
            'invoice_date': data.get('invoice_date', ''),
            'due_date': data.get('due_date', ''),
            'total_amount': data.get('total_amount', data.get('amount', '')),
            'tax_amount': data.get('tax', data.get('tax_amount', '')),
            'currency': data.get('currency', 'USD'),
            'payment_terms': data.get('payment_terms', '')
        })
    
    # Convert amounts to numbers if they're strings
    for amount_field in ['total_amount', 'tax_amount']:
        if result[amount_field]:
            try:
                # Extract numeric value if it's a string with text
                amount_str = str(result[amount_field])
                # Extract numbers
                numbers = re.findall(r'\d+\.?\d*', amount_str)
                if numbers:
                    result[amount_field] = float(numbers[0])
                else:
                    result[amount_field] = ''
            except (ValueError, AttributeError):
                result[amount_field] = ''
    
    # Clean up extracted data
    result = clean_extracted_data(result)
    
    return result

def extract_with_regex(text: str) -> dict:
    """Extract invoice data using regex patterns as fallback"""
    result = {
        'vendor_name': '',
        'invoice_number': '',
        'invoice_date': '',
        'due_date': '',
        'total_amount': '',
        'tax_amount': '',
        'currency': 'USD',
        'payment_terms': ''
    }
    
    patterns = {
        'invoice_number': [
            r'["\']invoice[_\s]*number["\']?\s*:?\s*["\']?([A-Z0-9\-]+)["\']?',
            r'Invoice\s*#?:?\s*([A-Z0-9\-]+)',
            r'INV[A-Z]*[-\s]?(\d{4}[-\s]\d{4})'
        ],
        'vendor_name': [
            r'["\']vendor[_\s]*name["\']?\s*:?\s*["\']?([^"\'}\n]+)["\']?',
            r'From:\s*([^\n]+)',
            r'Bill\s*From:\s*([^\n]+)'
        ],
        'invoice_date': [
            r'["\']invoice[_\s]*date["\']?\s*:?\s*["\']?(\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4})["\']?',
            r'Date:\s*(\d{2}/\d{2}/\d{4}|\d{4}-\d{2}-\d{2})',
            r'Dated:\s*(\d{2}/\d{2}/\d{4}|\d{4}-\d{2}-\d{2})'
        ],
        'due_date': [
            r'["\']due[_\s]*date["\']?\s*:?\s*["\']?(\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4})["\']?',
            r'Due:\s*(\d{2}/\d{2}/\d{4}|\d{4}-\d{2}-\d{2})',
            r'Due\s*Date:\s*(\d{2}/\d{2}/\d{4}|\d{4}-\d{2}-\d{2})'
        ],
        'total_amount': [
            r'["\']total[_\s]*amount["\']?\s*:?\s*["\']?(\d+\.?\d*)["\']?',
            r'["\']amount["\']?\s*:?\s*["\']?(\d+\.?\d*)["\']?',
            r'Total:\s*\$?(\d+\.?\d*)',
            r'Amount:\s*\$?(\d+\.?\d*)'
        ],
        'currency': [
            r'["\']currency["\']?\s*:?\s*["\']?([A-Z]{3})["\']?'
        ]
    }
    
    for field, pattern_list in patterns.items():
        for pattern in pattern_list:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                result[field] = match.group(1).strip()
                break
    
    return result

def export_to_excel(result: dict, filename: str = "processed_invoices.xlsx") -> str:
    """Export processed invoice to Excel file"""
    try:
        # Extract invoice data
        if result.get('result'):
            result_str = str(result['result'])
            invoice_data = extract_invoice_data_from_json(result_str)
        else:
            invoice_data = {}
        
        # Create row data
        row_data = {
            'Processed Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Status': result.get('status', 'unknown'),
            'PDF Path': result.get('invoice_path', ''),
            'Vendor Name': invoice_data.get('vendor_name', 'Unknown'),
            'Invoice Number': invoice_data.get('invoice_number', ''),
            'Invoice Date': invoice_data.get('invoice_date', ''),
            'Due Date': invoice_data.get('due_date', ''),
            'Amount': invoice_data.get('total_amount', ''),
            'Currency': invoice_data.get('currency', 'USD'),
            'Tax Amount': invoice_data.get('tax_amount', ''),
            'Payment Terms': invoice_data.get('payment_terms', ''),
            'Model Used': result.get('model_used', 'unknown'),
            'Processing Time': result.get('processing_time', '')
        }
        
        # Create DataFrame
        df = pd.DataFrame([row_data])
        
        # Check if file exists
        try:
            existing_df = pd.read_excel(filename)
            # Append to existing
            df = pd.concat([existing_df, df], ignore_index=True)
            logger.info("✅ Appended to existing Excel file")
        except FileNotFoundError:
            logger.info("✅ Creating new Excel file")
        
        # Export to Excel
        df.to_excel(filename, index=False, sheet_name='Processed Invoices')
        logger.info(f"✅ Exported to Excel: {filename}")
        
        return filename
        
    except Exception as e:
        logger.error(f"❌ Error exporting to Excel: {str(e)}")
        raise
