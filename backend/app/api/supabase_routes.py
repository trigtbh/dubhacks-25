from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from app.services.supabase_client import get_supabase_client
from supabase import Client

router = APIRouter(prefix="/supabase", tags=["supabase"])

def require_supabase() -> Client:
    """Dependency to ensure Supabase is configured"""
    client = get_supabase_client()
    if client is None:
        raise HTTPException(
            status_code=503,
            detail="Supabase is not configured. Please set SUPABASE_URL and SUPABASE_KEY in your .env file."
        )
    return client

@router.get("/status")
async def supabase_status(supabase: Optional[Client] = Depends(lambda: get_supabase_client())):
    """Check Supabase connection status"""
    if supabase is None:
        return {
            "configured": False,
            "message": "Supabase is not configured. Add SUPABASE_URL and SUPABASE_KEY to .env file."
        }
    
    try:
        # Simple test query - this will fail gracefully if no tables exist yet
        return {
            "configured": True,
            "status": "connected",
            "message": "Supabase is properly configured and connected"
        }
    except Exception as e:
        return {
            "configured": True,
            "status": "error",
            "message": f"Supabase configuration error: {str(e)}"
        }

# Example endpoints demonstrating Supabase usage
# Uncomment and modify these once you have tables set up

# @router.get("/example")
# async def get_example_data(supabase: Client = Depends(require_supabase)):
#     """Example: Get data from a Supabase table"""
#     try:
#         response = supabase.table('your_table_name').select("*").limit(10).execute()
#         return {"data": response.data}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @router.post("/example")
# async def create_example_data(
#     data: dict,
#     supabase: Client = Depends(require_supabase)
# ):
#     """Example: Insert data into a Supabase table"""
#     try:
#         response = supabase.table('your_table_name').insert(data).execute()
#         return {"data": response.data}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

