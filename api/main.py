from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
import uvicorn
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Invoice Processing Agent API",
    description="AI-powered invoice processing with multi-agent system",
    version="1.0.0"
)

# ============================================================================
# ROOT ENDPOINT - This fixes the "Not Found" error
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "service": "Invoice Processing Agent API",
        "version": "1.0.0",
        "status": "running",
        "description": "AI-powered invoice processing using Google ADK agents",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "process_invoice": "/api/v1/invoices/process",
            "batch_process": "/api/v1/invoices/batch",
            "invoice_status": "/api/v1/invoices/{invoice_id}/status"
        },
        "documentation": "Visit /docs for interactive API documentation"
    }

# ============================================================================
# HEALTH CHECK ENDPOINT
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Invoice Processing Agent",
        "version": "1.0.0"
    }

# ============================================================================
# INVOICE PROCESSING ENDPOINTS
# ============================================================================

@app.post("/api/v1/invoices/process")
async def process_invoice(
    file: UploadFile = File(...),
    vendor_name: Optional[str] = None
):
    """
    Process a single invoice PDF through the agent pipeline.
    
    Args:
        file: Invoice PDF file
        vendor_name: Optional vendor name for context
        
    Returns:
        Processing results with all agent decisions
    """
    try:
        logger.info(f"📄 Processing invoice: {file.filename}")
        
        # Validate file type
        if not file.filename.endswith('.pdf'):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are supported"
            )
        
        # Save uploaded file temporarily
        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        logger.info(f"✅ File saved to: {temp_path}")
        
        # TODO: Import and use orchestrator
        # from agents.orchestrator import InvoiceOrchestrator
        # orchestrator = InvoiceOrchestrator()
        # result = orchestrator.process_invoice(temp_path, vendor_name)
        
        # For now, return mock response
        return {
            "status": "success",
            "message": "Invoice processing endpoint is working",
            "filename": file.filename,
            "vendor_name": vendor_name,
            "note": "Agent processing will be implemented here"
        }
        
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"❌ Error processing invoice: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error processing invoice: {str(e)}"
        )

@app.post("/api/v1/invoices/batch")
async def batch_process_invoices(
    files: list[UploadFile] = File(...)
):
    """
    Process multiple invoices in batch.
    
    Args:
        files: List of invoice PDF files
        
    Returns:
        Batch processing results
    """
    try:
        logger.info(f"📄 Batch processing {len(files)} invoices")
        
        results = []
        for file in files:
            if not file.filename.endswith('.pdf'):
                results.append({
                    "filename": file.filename,
                    "status": "error",
                    "error": "Only PDF files are supported"
                })
                continue
            
            results.append({
                "filename": file.filename,
                "status": "success",
                "message": "Batch processing endpoint is working"
            })
        
        return {
            "status": "success",
            "total_files": len(files),
            "results": results
        }
        
    except Exception as e:
        logger.error(f"❌ Error in batch processing: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error in batch processing: {str(e)}"
        )

@app.get("/api/v1/invoices/{invoice_id}/status")
async def get_invoice_status(invoice_id: str):
    """
    Get processing status of an invoice.
    
    Args:
        invoice_id: Unique invoice identifier
        
    Returns:
        Invoice processing status
    """
    try:
        logger.info(f"📊 Getting status for invoice: {invoice_id}")
        
        # TODO: Implement actual status lookup
        return {
            "invoice_id": invoice_id,
            "status": "completed",
            "message": "Status endpoint is working",
            "note": "Status lookup will be implemented here"
        }
        
    except Exception as e:
        logger.error(f"❌ Error getting status: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error getting status: {str(e)}"
        )

# ============================================================================
# STARTUP EVENT
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Run on API startup"""
    logger.info("=" * 60)
    logger.info("🚀 Invoice Processing Agent API Starting...")
    logger.info("=" * 60)
    logger.info(f"   Environment: {os.getenv('ENVIRONMENT', 'development')}")
    logger.info(f"   Port: {os.getenv('API_PORT', '8080')}")
    logger.info("=" * 60)

@app.on_event("shutdown")
async def shutdown_event():
    """Run on API shutdown"""
    logger.info("=" * 60)
    logger.info("🛑 Invoice Processing Agent API Shutting Down...")
    logger.info("=" * 60)

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    port = int(os.getenv("API_PORT", "8080"))
    host = os.getenv("API_HOST", "0.0.0.0")
    
    logger.info(f"Starting server on {host}:{port}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )