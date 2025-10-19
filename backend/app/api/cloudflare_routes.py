from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from app.services.cloudflare_client import get_d1_client, get_kv_client, get_r2_client, CloudflareD1Client, CloudflareKVClient, CloudflareR2Client
from app.dependencies import get_current_user

router = APIRouter(prefix="/cloudflare", tags=["cloudflare"], dependencies=[Depends(get_current_user)])

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

# ===== R2 Object Storage Endpoints =====

def require_r2() -> CloudflareR2Client:
    """Dependency to ensure R2 is configured"""
    client = get_r2_client()
    if client is None:
        raise HTTPException(
            status_code=503,
            detail="Cloudflare R2 is not configured. Please set CLOUDFLARE_R2_ACCOUNT_ID, CLOUDFLARE_R2_ACCESS_KEY_ID, CLOUDFLARE_R2_SECRET_ACCESS_KEY, and CLOUDFLARE_R2_BUCKET_NAME in your .env file."
        )
    return client

@router.get("/r2/status")
async def r2_status():
    """Check Cloudflare R2 storage status"""
    client = get_r2_client()
    if client is None:
        return {
            "configured": False,
            "message": "R2 is not configured. Add R2 credentials to .env file."
        }
    
    return {
        "configured": True,
        "status": "ready",
        "message": "Cloudflare R2 is properly configured"
    }

class PresignedUploadRequest(BaseModel):
    key: str
    expires_in: int = 3600
    content_type: Optional[str] = None

class PresignedDownloadRequest(BaseModel):
    key: str
    expires_in: int = 3600
    filename: Optional[str] = None

@router.post("/r2/presigned-upload-url")
async def generate_presigned_upload_url(
    request: PresignedUploadRequest,
    r2: CloudflareR2Client = Depends(require_r2)
):
    """
    Generate a presigned URL for uploading a file to R2
    
    Example:
    ```json
    {
        "key": "uploads/document.pdf",
        "expires_in": 3600,
        "content_type": "application/pdf"
    }
    ```
    
    Returns a presigned URL that can be used to PUT the file directly to R2.
    The client should use PUT method with the file data in the request body.
    """
    try:
        url = await r2.generate_presigned_upload_url(
            request.key,
            request.expires_in,
            request.content_type
        )
        return {
            "success": True,
            "url": url,
            "key": request.key,
            "method": "PUT",
            "expires_in": request.expires_in
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/r2/presigned-download-url")
async def generate_presigned_download_url(
    request: PresignedDownloadRequest,
    r2: CloudflareR2Client = Depends(require_r2)
):
    """
    Generate a presigned URL for downloading a file from R2
    
    Example:
    ```json
    {
        "key": "uploads/document.pdf",
        "expires_in": 3600,
        "filename": "my-document.pdf"
    }
    ```
    
    Returns a presigned URL that can be used to GET the file directly from R2.
    """
    try:
        url = await r2.generate_presigned_download_url(
            request.key,
            request.expires_in,
            request.filename
        )
        return {
            "success": True,
            "url": url,
            "key": request.key,
            "method": "GET",
            "expires_in": request.expires_in
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/r2/upload")
async def upload_file_to_r2(
    key: str,
    file: UploadFile = File(...),
    r2: CloudflareR2Client = Depends(require_r2)
):
    """
    Upload a file directly to R2 through the backend
    
    This endpoint allows uploading files through the backend API.
    For client-side uploads, use the presigned URL endpoints instead.
    """
    try:
        content = await file.read()
        await r2.upload_file(key, content, file.content_type)
        return {
            "success": True,
            "key": key,
            "filename": file.filename,
            "size": len(content)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/r2/download/{key:path}")
async def download_file_from_r2(
    key: str,
    r2: CloudflareR2Client = Depends(require_r2)
):
    """
    Download a file directly from R2 through the backend
    
    For client-side downloads, use the presigned URL endpoints instead.
    """
    try:
        from fastapi.responses import Response
        data = await r2.download_file(key)
        return Response(content=data, media_type="application/octet-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/r2/{key:path}")
async def delete_file_from_r2(
    key: str,
    r2: CloudflareR2Client = Depends(require_r2)
):
    """Delete a file from R2"""
    try:
        await r2.delete_file(key)
        return {"success": True, "key": key}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/r2/list")
async def list_files_in_r2(
    prefix: Optional[str] = None,
    max_keys: int = 100,
    r2: CloudflareR2Client = Depends(require_r2)
):
    """
    List files in the R2 bucket
    
    Query parameters:
    - prefix: Filter files by prefix (optional)
    - max_keys: Maximum number of files to return (default: 100)
    """
    try:
        files = await r2.list_files(prefix, max_keys)
        return {
            "success": True,
            "files": files,
            "count": len(files)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== Example/Demo Endpoints =====

@router.get("/info")
async def cloudflare_info():
    """Get information about configured Cloudflare services"""
    d1_client = get_d1_client()
    kv_client = get_kv_client()
    r2_client = get_r2_client()
    
    return {
        "services": {
            "d1_database": {
                "configured": d1_client is not None,
                "description": "SQLite-compatible database"
            },
            "kv_storage": {
                "configured": kv_client is not None,
                "description": "Key-value storage"
            },
            "r2_storage": {
                "configured": r2_client is not None,
                "description": "Object storage (S3-compatible)"
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
            ],
            "r2": [
                "GET /cloudflare/r2/status",
                "POST /cloudflare/r2/presigned-upload-url",
                "POST /cloudflare/r2/presigned-download-url",
                "POST /cloudflare/r2/upload",
                "GET /cloudflare/r2/download/{key}",
                "DELETE /cloudflare/r2/{key}",
                "GET /cloudflare/r2/list",
                "GET /cloudflare/r2/test - Full workflow demo"
            ]
        }
    }


@router.get("/r2/test")
async def test_r2_presigned_workflow(r2: CloudflareR2Client = Depends(require_r2)):
    """
    Test endpoint that demonstrates the complete R2 presigned URL workflow:
    1. Generates a sample image
    2. Gets a presigned upload URL
    3. Uploads the image using the presigned URL
    4. Returns a presigned download URL to view the uploaded image
    
    Returns:
    - upload_url: The presigned URL used for uploading
    - download_url: A presigned URL you can visit to download/view the image
    - key: The object key where the image was stored
    - image_info: Details about the generated image
    """
    try:
        from PIL import Image, ImageDraw, ImageFont
        import io
        from datetime import datetime
        import httpx
        
        # Step 1: Generate a sample image
        width, height = 400, 300
        image = Image.new('RGB', (width, height), color='#4A90E2')
        draw = ImageDraw.Draw(image)
        
        # Draw some test content
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Draw rectangles
        draw.rectangle([50, 50, 350, 100], fill='#FFFFFF', outline='#2C5F8D', width=3)
        draw.rectangle([50, 120, 350, 250], fill='#E8F4F8', outline='#2C5F8D', width=2)
        
        # Add text
        try:
            # Try to use a default font (may vary by system)
            font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
            font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
        except:
            # Fallback to default font
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        draw.text((75, 65), "R2 Presigned URL Test", fill='#2C5F8D', font=font_large)
        draw.text((60, 140), f"Generated: {timestamp}", fill='#333333', font=font_small)
        draw.text((60, 170), "This image was uploaded via", fill='#333333', font=font_small)
        draw.text((60, 195), "presigned URL to Cloudflare R2", fill='#333333', font=font_small)
        
        # Convert image to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        image_data = img_byte_arr.getvalue()
        
        # Step 2: Generate presigned upload URL
        key = f"test-images/sample-{datetime.now().strftime('%Y%m%d-%H%M%S')}.png"
        upload_url = await r2.generate_presigned_upload_url(
            key=key,
            expires_in=3600,
            content_type="image/png"
        )
        
        # Step 3: Upload the image using the presigned URL
        async with httpx.AsyncClient() as client:
            upload_response = await client.put(
                upload_url,
                content=image_data,
                headers={"Content-Type": "image/png"},
                timeout=30.0
            )
            upload_response.raise_for_status()
        
        # Step 4: Generate presigned download URL
        download_url = await r2.generate_presigned_download_url(
            key=key,
            expires_in=3600,
            filename="sample-test.png"
        )
        
        return {
            "success": True,
            "message": "Successfully uploaded test image using presigned URL workflow",
            "workflow": {
                "step_1": "Generated sample PNG image",
                "step_2": "Obtained presigned upload URL",
                "step_3": "Uploaded image to R2 via presigned URL",
                "step_4": "Generated presigned download URL"
            },
            "key": key,
            "upload_url": upload_url,
            "download_url": download_url,
            "image_info": {
                "format": "PNG",
                "size_bytes": len(image_data),
                "dimensions": f"{width}x{height}",
                "generated_at": timestamp
            },
            "instructions": {
                "view_image": f"Visit the download_url to view the uploaded image",
                "direct_link": download_url
            }
        }
        
    except Exception as e:
        import traceback
        raise HTTPException(
            status_code=500, 
            detail={
                "error": str(e),
                "traceback": traceback.format_exc()
            }
        )

