from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime
from app.dependencies import get_current_user

router = APIRouter(dependencies=[Depends(get_current_user)])

class UnfreezeRequest(BaseModel):
    text: str

class UnfreezeResponse(BaseModel):
    message: str
    input: str
    timestamp: str

@router.post("/unfreeze", response_model=UnfreezeResponse)
async def unfreeze(request: UnfreezeRequest):
    """
    Process the unfreeze request
    This is a placeholder endpoint - add your logic here
    """
    if not request.text or not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    # Process the text (placeholder logic)
    processed_text = f"Successfully unfroze: {request.text}"
    
    return UnfreezeResponse(
        message=processed_text,
        input=request.text,
        timestamp=datetime.now().isoformat()
    )

@router.get("/status")
async def get_status():
    """Get API status"""
    return {
        "status": "operational",
        "endpoints": {
            "POST /unfreeze": "Process unfreeze requests",
            "GET /status": "Get API status"
        },
        "timestamp": datetime.now().isoformat()
    }

