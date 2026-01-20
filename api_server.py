from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fairprop import FairHousingAuditor
from typing import List, Optional
import logging
from datetime import datetime
import json
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fairprop.api")

app = FastAPI(
    title="FairProp Compliance API",
    description="REST API for Fair Housing Act compliance checking across 100+ global jurisdictions",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for browser extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize auditor (singleton for performance)
auditor = FairHousingAuditor()

# Usage tracking
usage_log_path = Path("logs/api_usage.jsonl")
usage_log_path.parent.mkdir(exist_ok=True)

class ScanRequest(BaseModel):
    text: str
    jurisdictions: List[str] = []
    use_cache: bool = True

class ScanResponse(BaseModel):
    score: int
    is_safe: bool
    flagged_items: list

class BatchScanRequest(BaseModel):
    items: List[ScanRequest]

class BatchScanResponse(BaseModel):
    results: List[ScanResponse]
    total_scanned: int
    total_violations: int

def log_usage(endpoint: str, request_data: dict, response_data: dict):
    """Log API usage for analytics (runs in background)."""
    try:
        log_entry = {
            "timestamp": datetime.now(datetime.UTC).isoformat(),
            "endpoint": endpoint,
            "request": request_data,
            "response": {
                "score": response_data.get("score"),
                "is_safe": response_data.get("is_safe"),
                "violations_count": len(response_data.get("flagged_items", []))
            }
        }
        with open(usage_log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')
    except Exception as e:
        logger.error(f"Failed to log usage: {e}")

@app.post("/api/scan", response_model=ScanResponse)
async def scan_text(request: ScanRequest, background_tasks: BackgroundTasks):
    """
    Scan a single text for Fair Housing Act violations.
    
    Supports 100+ jurisdictions across 6 continents.
    Uses caching by default for improved performance.
    """
    try:
        if request.jurisdictions:
            # Create jurisdiction-specific auditor
            auditor_with_jurisdiction = FairHousingAuditor(jurisdictions=request.jurisdictions)
            report = auditor_with_jurisdiction.scan_text(request.text, use_cache=request.use_cache)
        else:
            report = auditor.scan_text(request.text, use_cache=request.use_cache)
        
        # Log usage in background
        background_tasks.add_task(
            log_usage,
            "/api/scan",
            {"jurisdictions": request.jurisdictions, "text_length": len(request.text)},
            report
        )
        
        return ScanResponse(**report)
    except Exception as e:
        logger.error(f"Scan failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/scan/batch", response_model=BatchScanResponse)
async def scan_batch(request: BatchScanRequest, background_tasks: BackgroundTasks):
    """
    Batch scan multiple texts for improved efficiency.
    
    Useful for processing large volumes of listings.
    Each item can have different jurisdictions.
    """
    try:
        results = []
        total_violations = 0
        
        for item in request.items:
            if item.jurisdictions:
                auditor_temp = FairHousingAuditor(jurisdictions=item.jurisdictions)
                report = auditor_temp.scan_text(item.text, use_cache=item.use_cache)
            else:
                report = auditor.scan_text(item.text, use_cache=item.use_cache)
            
            results.append(ScanResponse(**report))
            if not report['is_safe']:
                total_violations += 1
        
        # Log batch usage
        background_tasks.add_task(
            log_usage,
            "/api/scan/batch",
            {"batch_size": len(request.items)},
            {"total_violations": total_violations}
        )
        
        return BatchScanResponse(
            results=results,
            total_scanned=len(results),
            total_violations=total_violations
        )
    except Exception as e:
        logger.error(f"Batch scan failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/reload-rules")
async def reload_rules():
    """
    Hot-reload rules from disk without restarting the service.
    
    Useful for updating rules in production without downtime.
    """
    try:
        result = auditor.reload_rules()
        return {
            "status": "success",
            "message": f"Rules reloaded: {result['old_count']} → {result['new_count']}",
            **result
        }
    except Exception as e:
        logger.error(f"Rule reload failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """Health check endpoint with system status."""
    return {
        "status": "healthy",
        "service": "FairProp API",
        "version": "2.0.0",
        "ai_available": auditor.model_manager.has_ai,
        "rules_loaded": len(auditor.rules),
        "jurisdictions_supported": "100+"
    }

@app.get("/api/stats")
async def get_stats():
    """Get API usage statistics."""
    try:
        if not usage_log_path.exists():
            return {"total_scans": 0, "message": "No usage data yet"}
        
        total_scans = 0
        total_violations = 0
        
        with open(usage_log_path, 'r', encoding='utf-8') as f:
            for line in f:
                entry = json.loads(line)
                total_scans += 1
                if not entry['response'].get('is_safe', True):
                    total_violations += 1
        
        return {
            "total_scans": total_scans,
            "total_violations": total_violations,
            "violation_rate": f"{(total_violations/total_scans*100):.1f}%" if total_scans > 0 else "0%"
        }
    except Exception as e:
        logger.error(f"Stats retrieval failed: {e}")
        return {"error": str(e)}

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "service": "FairProp Compliance API",
        "version": "2.0.0",
        "description": "Global fair housing compliance checking",
        "coverage": "100+ jurisdictions across 6 continents",
        "docs": "/docs",
        "health": "/api/health",
        "stats": "/api/stats"
    }

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting FairProp API server...")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

