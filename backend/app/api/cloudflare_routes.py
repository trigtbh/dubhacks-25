from fastapi import APIRouter, HTTPException, Depends
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from app.services.cloudflare_client import get_d1_client, get_kv_client, CloudflareD1Client, CloudflareKVClient

router = APIRouter(prefix="/cloudflare", tags=["cloudflare"])

# ===== D1 Database Endpoints =====

def require_d1() -> CloudflareD1Client:
    """Dependency to ensure D1 is configured"""
    client = get_d1_client()
    if client is None:
        raise HTTPException(
            status_code=503,
            detail="Cloudflare D1 is not configured. Please set CLOUDFLARE_ACCOUNT_ID, CLOUDFLARE_API_TOKEN, and CLOUDFLARE_D1_DATABASE_ID in your .env file."
        )
    return client

@router.get("/d1/status")
async def d1_status():
    """Check Cloudflare D1 database connection status"""
    client = get_d1_client()
    if client is None:
        return {
            "configured": False,
            "message": "D1 is not configured. Add Cloudflare credentials to .env file."
        }
    
    try:
        # Test with a simple query
        result = await client.raw_query("SELECT 1 as test")
        return {
            "configured": True,
            "status": "connected",
            "message": "Cloudflare D1 is properly configured and connected",
            "test_result": result
        }
    except Exception as e:
        return {
            "configured": True,
            "status": "error",
            "message": f"D1 configuration error: {str(e)}"
        }

class D1QueryRequest(BaseModel):
    sql: str
    params: List[Any] = []

class D1BatchRequest(BaseModel):
    queries: List[Dict[str, Any]]  # List of {sql: str, params: List}

@router.post("/d1/query")
async def execute_d1_query(request: D1QueryRequest, d1: CloudflareD1Client = Depends(require_d1)):
    """
    Execute a SQL query on D1 database
    
    Example:
    ```json
    {
        "sql": "SELECT * FROM users WHERE id = ?",
        "params": [1]
    }
    ```
    """
    try:
        result = await d1.query(request.sql, request.params)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/d1/batch")
async def execute_d1_batch(request: D1BatchRequest, d1: CloudflareD1Client = Depends(require_d1)):
    """
    Execute multiple SQL queries in a batch
    
    Example:
    ```json
    {
        "queries": [
            {"sql": "INSERT INTO users (name) VALUES (?)", "params": ["John"]},
            {"sql": "SELECT * FROM users", "params": []}
        ]
    }
    ```
    """
    try:
        queries = [(q["sql"], q.get("params", [])) for q in request.queries]
        result = await d1.batch(queries)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== KV Storage Endpoints =====

def require_kv() -> CloudflareKVClient:
    """Dependency to ensure KV is configured"""
    client = get_kv_client()
    if client is None:
        raise HTTPException(
            status_code=503,
            detail="Cloudflare KV is not configured. Please set CLOUDFLARE_KV_NAMESPACE_ID in your .env file."
        )
    return client

@router.get("/kv/status")
async def kv_status():
    """Check Cloudflare KV storage status"""
    client = get_kv_client()
    if client is None:
        return {
            "configured": False,
            "message": "KV is not configured. Add CLOUDFLARE_KV_NAMESPACE_ID to .env file."
        }
    
    return {
        "configured": True,
        "status": "ready",
        "message": "Cloudflare KV is properly configured"
    }

class KVPutRequest(BaseModel):
    key: str
    value: str
    expiration_ttl: Optional[int] = None

@router.get("/kv/{key}")
async def get_kv_value(key: str, kv: CloudflareKVClient = Depends(require_kv)):
    """Get a value from KV storage"""
    try:
        value = await kv.get(key)
        if value is None:
            raise HTTPException(status_code=404, detail="Key not found")
        return {"key": key, "value": value}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/kv")
async def put_kv_value(request: KVPutRequest, kv: CloudflareKVClient = Depends(require_kv)):
    """
    Store a value in KV storage
    
    Example:
    ```json
    {
        "key": "user:123",
        "value": "John Doe",
        "expiration_ttl": 3600
    }
    ```
    """
    try:
        await kv.put(request.key, request.value, request.expiration_ttl)
        return {"success": True, "key": request.key}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/kv/{key}")
async def delete_kv_value(key: str, kv: CloudflareKVClient = Depends(require_kv)):
    """Delete a value from KV storage"""
    try:
        await kv.delete(key)
        return {"success": True, "key": key}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/kv/list/keys")
async def list_kv_keys(prefix: Optional[str] = None, limit: int = 100, kv: CloudflareKVClient = Depends(require_kv)):
    """List keys in KV storage"""
    try:
        keys = await kv.list_keys(prefix, limit)
        return {"keys": keys, "count": len(keys)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== Example/Demo Endpoints =====

@router.get("/info")
async def cloudflare_info():
    """Get information about configured Cloudflare services"""
    d1_client = get_d1_client()
    kv_client = get_kv_client()
    
    return {
        "services": {
            "d1_database": {
                "configured": d1_client is not None,
                "description": "SQLite-compatible database"
            },
            "kv_storage": {
                "configured": kv_client is not None,
                "description": "Key-value storage"
            }
        },
        "endpoints": {
            "d1": [
                "GET /cloudflare/d1/status",
                "POST /cloudflare/d1/query",
                "POST /cloudflare/d1/batch"
            ],
            "kv": [
                "GET /cloudflare/kv/status",
                "GET /cloudflare/kv/{key}",
                "PUT /cloudflare/kv",
                "DELETE /cloudflare/kv/{key}",
                "GET /cloudflare/kv/list/keys"
            ]
        }
    }

