"""Excel Export Utility for Invoice Processing"""
import pandas as pd
from datetime import datetime
import os
import json
import logging
import re

logger = logging.getLogger(__name__)

def parse_invoice_result(result_text: str) -> dict:
    """Parse the JSON result from invoice processing with improved extraction"""
    try:
        if not result_text:
            return {}
            
        # Try to find JSON in markdown code blocks first
        json_match = re.search(r'``````', result_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
            data = json.loads(json_str)
            return data
        
        # Try to find JSON without code blocks
        json_match = re.search(r'(\{[^{}]*"stages"[^{}]*\{.*?\}[^{}]*\})', result_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
            # Clean up any markdown artifacts
            json_str = json_str.replace('``````', '')
            data = json.loads(json_str)
            return data
            
        # Last resort: try to parse the entire result as JSON
        if result_text.strip().startswith('{'):
            data = json.loads(result_text)
            return data
            
        return {}
        
    except json.JSONDecodeError as e:
        logger.warning(f"JSON decode error: {e}")
        # Try to extract key fields with regex as fallback
        return extract_with_regex(result_text)
    except Exception as e:
        logger.warning(f"Could not parse result: {e}")
        return {}

def extract_with_regex(text: str) -> dict:
    """Extract invoice data using regex patterns as fallback"""
    data = {}
    
    # Extract invoice number
    inv_match = re.search(r'"invoice_number":\s*"([^"]+)"', text)
    if inv_match:
        data['invoice_number'] = inv_match.group(1)
    
    # Extract vendor name
    vendor_match = re.search(r'"vendor_name":\s*"([^"]+)"', text)
    if vendor_match:
        data['vendor_name'] = vendor_match.group(1)
    
    # Extract dates
    date_match = re.search(r'"invoice_date":\s*"([^"]+)"', text)
    if date_match:
        data['invoice_date'] = date_match.group(1)
    
    due_match = re.search(r'"due_date":\s*"([^"]+)"', text)
    if due_match:
        data['due_date'] = due_match.group(1)
    
    # Extract amount (try multiple patterns)
    amount_patterns = [
        r'"total_amount":\s*(\d+\.?\d*)',
        r'"amount_total":\s*(\d+\.?\d*)',
        r'"amount":\s*(\d+\.?\d*)'
    ]
    for pattern in amount_patterns:
        amount_match = re.search(pattern, text)
        if amount_match:
            data['total_amount'] = float(amount_match.group(1))
            break
    
    # Extract currency
    curr_match = re.search(r'"currency":\s*"([^"]+)"', text)
    if curr_match:
        data['currency'] = curr_match.group(1)
    
    # Extract tax
    tax_match = re.search(r'"tax_amount":\s*(\d+\.?\d*)', text)
    if tax_match:
        data['tax_amount'] = float(tax_match.group(1))
    
    # Extract payment terms
    terms_match = re.search(r'"payment_terms":\s*"([^"]+)"', text)
    if terms_match:
        data['payment_terms'] = terms_match.group(1)
    
    return data

def extract_invoice_data(invoice_result: dict) -> dict:
    """Extract invoice data from various possible locations in result"""
    
    # Parse the result text
    parsed_data = {}
    if 'result' in invoice_result:
        parsed_data = parse_invoice_result(invoice_result['result'])
    
    # Try to get data from stages
    invoice_data = {}
    if parsed_data and 'stages' in parsed_data:
        # Look through stages for extracted data
        for stage in parsed_data.get('stages', []):
            if 'data_extracted' in stage:
                invoice_data.update(stage['data_extracted'])
            elif 'stage_name' in stage and stage['stage_name'] == 'CAPTURE':
                invoice_data.update(stage.get('data_extracted', {}))
    
    # If no data from stages, try direct extraction from parsed_data
    if not invoice_data and parsed_data:
        invoice_data = parsed_data
    
    # Fallback: try regex extraction on raw result
    if not invoice_data and 'result' in invoice_result:
        invoice_data = extract_with_regex(invoice_result['result'])
    
    return invoice_data

def export_to_excel(invoice_result: dict, output_path: str = "processed_invoices.xlsx") -> str:
    """
    Export processed invoice data to Excel with improved data extraction
    
    Args:
        invoice_result: Result from orchestrator.process_invoice()
        output_path: Path to save Excel file
        
    Returns:
        Path to saved Excel file
    """
    try:
        # Extract invoice data using improved parser
        invoice_data = extract_invoice_data(invoice_result)
        
        # Get vendor name from result or data
        vendor_name = invoice_result.get('vendor_name', '')
        if not vendor_name:
            vendor_name = invoice_data.get('vendor_name', 'Unknown')
        
        # Create DataFrame with invoice data
        df = pd.DataFrame([{
            'Processed Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Status': invoice_result.get('status', 'unknown'),
            'PDF Path': invoice_result.get('pdf_path', ''),
            'Vendor Name': vendor_name,
            'Invoice Number': invoice_data.get('invoice_number', 'N/A'),
            'Invoice Date': invoice_data.get('invoice_date', 'N/A'),
            'Due Date': invoice_data.get('due_date', 'N/A'),
            'Amount': invoice_data.get('total_amount', invoice_data.get('amount_total', invoice_data.get('amount', 0))),
            'Currency': invoice_data.get('currency', 'USD'),
            'Tax Amount': invoice_data.get('tax_amount', 0),
            'Payment Terms': invoice_data.get('payment_terms', 'N/A'),
            'Model Used': invoice_result.get('model_used', 'unknown'),
            'Processing Time': '~2 seconds'
        }])
        
        # Append to existing file or create new
        if os.path.exists(output_path):
            try:
                existing_df = pd.read_excel(output_path, engine='openpyxl')
                df = pd.concat([existing_df, df], ignore_index=True)
                logger.info(f"✅ Appended to existing Excel file")
            except Exception as e:
                logger.warning(f"Could not read existing file, creating new: {e}")
        else:
            logger.info(f"✅ Creating new Excel file")
        
        # Save to Excel with auto-adjusted column widths
        writer = pd.ExcelWriter(output_path, engine='openpyxl')
        df.to_excel(writer, index=False, sheet_name='Processed Invoices')
        
        # Auto-adjust column widths
        worksheet = writer.sheets['Processed Invoices']
        for idx, col in enumerate(df.columns):
            max_length = max(
                df[col].astype(str).apply(len).max(),
                len(col)
            ) + 2
            worksheet.column_dimensions[chr(65 + idx)].width = min(max_length, 50)
        
        writer.close()
        
        logger.info(f"✅ Exported to Excel: {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"❌ Error exporting to Excel: {e}", exc_info=True)
        return None

def create_excel_report(invoices: list, output_path: str = "invoice_report.xlsx") -> str:
    """
    Create comprehensive Excel report from multiple invoices
    
    Args:
        invoices: List of invoice results
        output_path: Path to save report
        
    Returns:
        Path to saved report
    """
    try:
        rows = []
        for inv in invoices:
            invoice_data = extract_invoice_data(inv)
            vendor_name = inv.get('vendor_name', invoice_data.get('vendor_name', 'Unknown'))
            
            rows.append({
                'Date Processed': datetime.now().strftime('%Y-%m-%d'),
                'Status': inv.get('status'),
                'Vendor': vendor_name,
                'Invoice #': invoice_data.get('invoice_number', 'N/A'),
                'Amount': invoice_data.get('total_amount', invoice_data.get('amount_total', 0)),
                'Currency': invoice_data.get('currency', 'USD'),
                'Due Date': invoice_data.get('due_date', 'N/A')
            })
        
        df = pd.DataFrame(rows)
        
        # Save with formatting
        writer = pd.ExcelWriter(output_path, engine='openpyxl')
        df.to_excel(writer, index=False, sheet_name='Invoice Report')
        
        # Auto-adjust column widths
        worksheet = writer.sheets['Invoice Report']
        for idx, col in enumerate(df.columns):
            max_length = max(
                df[col].astype(str).apply(len).max(),
                len(col)
            ) + 2
            worksheet.column_dimensions[chr(65 + idx)].width = min(max_length, 30)
        
        writer.close()
        
        logger.info(f"✅ Created report: {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"❌ Error creating report: {e}", exc_info=True)
        return None
