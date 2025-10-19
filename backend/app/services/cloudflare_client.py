"""
Cloudflare D1 Database and Services Client

This client provides access to Cloudflare services while running on Oracle Cloud:
- D1 Database (SQLite-compatible)
- KV (Key-Value storage)
- R2 (Object storage)
"""

from typing import Optional, Any, Dict, List
import httpx
import aioboto3
from botocore.config import Config
from datetime import timedelta
from app.config import settings

class CloudflareD1Client:
    """
    Cloudflare D1 Database client for REST API access
    
    Usage:
        client = get_d1_client()
        if client:
            # Execute query
            result = await client.query("SELECT * FROM users WHERE id = ?", [uuid])
            
            # Execute multiple queries
            results = await client.batch([
                ("INSERT INTO users (name) VALUES (?)", ["John"]),
                ("SELECT * FROM users", [])
            ])
    """
    
    def __init__(self, account_id: str, api_token: str, database_id: str):
        self.account_id = account_id
        self.api_token = api_token
        self.database_id = database_id
        self.base_url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/d1/database/{database_id}"
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
    
    async def query(self, sql: str, params: List[Any] = None) -> Dict[str, Any]:
        """
        Execute a single SQL query
        
        Args:
            sql: SQL query string (use ? for parameters)
            params: List of parameters to bind to the query
            
        Returns:
            Dict with query results
        """
        async with httpx.AsyncClient() as client:
            payload = {
                "sql": sql,
                "params": params or []
            }
            response = await client.post(
                f"{self.base_url}/query",
                headers=self.headers,
                json=payload,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    
    async def batch(self, queries: List[tuple]) -> Dict[str, Any]:
        """
        Execute multiple SQL queries in a batch
        
        Args:
            queries: List of (sql, params) tuples
            
        Returns:
            Dict with batch results
        """
        async with httpx.AsyncClient() as client:
            payload = [
                {"sql": sql, "params": params or []}
                for sql, params in queries
            ]
            response = await client.post(
                f"{self.base_url}/query",
                headers=self.headers,
                json=payload,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    
    async def raw_query(self, sql: str) -> Dict[str, Any]:
        """Execute a raw SQL query without parameters"""
        return await self.query(sql, [])


class CloudflareKVClient:
    """
    Cloudflare KV (Key-Value) storage client
    
    Usage:
        kv = get_kv_client()
        if kv:
            # Store value
            await kv.put("key", "value")
            
            # Get value
            value = await kv.get("key")
            
            # Delete value
            await kv.delete("key")
    """
    
    def __init__(self, account_id: str, api_token: str, namespace_id: str):
        self.account_id = account_id
        self.api_token = api_token
        self.namespace_id = namespace_id
        self.base_url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/storage/kv/namespaces/{namespace_id}"
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
    
    async def get(self, key: str) -> Optional[str]:
        """Get a value from KV storage"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/values/{key}",
                headers=self.headers,
                timeout=10.0
            )
            if response.status_code == 404:
                return None
            response.raise_for_status()
            return response.text
    
    async def put(self, key: str, value: str, expiration_ttl: Optional[int] = None) -> bool:
        """
        Put a value into KV storage
        
        Args:
            key: The key to store
            value: The value to store
            expiration_ttl: Optional TTL in seconds
        """
        async with httpx.AsyncClient() as client:
            data = {"value": value}
            if expiration_ttl:
                data["expiration_ttl"] = expiration_ttl
            
            response = await client.put(
                f"{self.base_url}/values/{key}",
                headers=self.headers,
                json=data,
                timeout=10.0
            )
            response.raise_for_status()
            return True
    
    async def delete(self, key: str) -> bool:
        """Delete a value from KV storage"""
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{self.base_url}/values/{key}",
                headers=self.headers,
                timeout=10.0
            )
            response.raise_for_status()
            return True
    
    async def list_keys(self, prefix: Optional[str] = None, limit: int = 1000) -> List[str]:
        """List keys in the namespace"""
        async with httpx.AsyncClient() as client:
            params = {"limit": limit}
            if prefix:
                params["prefix"] = prefix
            
            response = await client.get(
                f"{self.base_url}/keys",
                headers=self.headers,
                params=params,
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()
            return [item["name"] for item in data.get("result", [])]


class CloudflareR2Client:
    """
    Cloudflare R2 (Object Storage) client using S3-compatible API
    
    Usage:
        r2 = get_r2_client()
        if r2:
            # Generate presigned URL for upload
            upload_url = await r2.generate_presigned_upload_url("myfile.pdf", expires_in=3600)
            
            # Generate presigned URL for download
            download_url = await r2.generate_presigned_download_url("myfile.pdf", expires_in=3600)
            
            # Upload file directly
            await r2.upload_file("myfile.pdf", file_data)
            
            # Download file directly
            data = await r2.download_file("myfile.pdf")
    """
    
    def __init__(self, account_id: str, access_key_id: str, secret_access_key: str, bucket_name: str):
        self.account_id = account_id
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.bucket_name = bucket_name
        self.endpoint_url = f"https://{account_id}.r2.cloudflarestorage.com"
        
        # Configure boto3 for R2
        self.config = Config(
            region_name='auto',
            signature_version='s3v4',
            s3={'addressing_style': 'path'}
        )
    
    def _get_session(self):
        """Get aioboto3 session"""
        return aioboto3.Session(
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key
        )
    
    async def generate_presigned_upload_url(
        self, 
        key: str, 
        expires_in: int = 3600,
        content_type: Optional[str] = None
    ) -> str:
        """
        Generate a presigned URL for uploading an object to R2
        
        Args:
            key: The object key (filename)
            expires_in: URL expiration time in seconds (default: 1 hour)
            content_type: Optional content type for the upload
            
        Returns:
            Presigned URL string
        """
        session = self._get_session()
        async with session.client('s3', endpoint_url=self.endpoint_url, config=self.config) as s3:
            params = {
                'Bucket': self.bucket_name,
                'Key': key
            }
            if content_type:
                params['ContentType'] = content_type
            
            url = await s3.generate_presigned_url(
                'put_object',
                Params=params,
                ExpiresIn=expires_in
            )
            return url
    
    async def generate_presigned_download_url(
        self, 
        key: str, 
        expires_in: int = 3600,
        filename: Optional[str] = None
    ) -> str:
        """
        Generate a presigned URL for downloading an object from R2
        
        Args:
            key: The object key (filename)
            expires_in: URL expiration time in seconds (default: 1 hour)
            filename: Optional filename for Content-Disposition header
            
        Returns:
            Presigned URL string
        """
        session = self._get_session()
        async with session.client('s3', endpoint_url=self.endpoint_url, config=self.config) as s3:
            params = {
                'Bucket': self.bucket_name,
                'Key': key
            }
            if filename:
                params['ResponseContentDisposition'] = f'attachment; filename="{filename}"'
            
            url = await s3.generate_presigned_url(
                'get_object',
                Params=params,
                ExpiresIn=expires_in
            )
            return url
    
    async def upload_file(self, key: str, data: bytes, content_type: Optional[str] = None) -> bool:
        """
        Upload a file directly to R2
        
        Args:
            key: The object key (filename)
            data: File data as bytes
            content_type: Optional content type
            
        Returns:
            True if successful
        """
        session = self._get_session()
        async with session.client('s3', endpoint_url=self.endpoint_url, config=self.config) as s3:
            params = {
                'Bucket': self.bucket_name,
                'Key': key,
                'Body': data
            }
            if content_type:
                params['ContentType'] = content_type
            
            await s3.put_object(**params)
            return True
    
    async def download_file(self, key: str) -> bytes:
        """
        Download a file directly from R2
        
        Args:
            key: The object key (filename)
            
        Returns:
            File data as bytes
        """
        session = self._get_session()
        async with session.client('s3', endpoint_url=self.endpoint_url, config=self.config) as s3:
            response = await s3.get_object(Bucket=self.bucket_name, Key=key)
            async with response['Body'] as stream:
                return await stream.read()
    
    async def delete_file(self, key: str) -> bool:
        """
        Delete a file from R2
        
        Args:
            key: The object key (filename)
            
        Returns:
            True if successful
        """
        session = self._get_session()
        async with session.client('s3', endpoint_url=self.endpoint_url, config=self.config) as s3:
            await s3.delete_object(Bucket=self.bucket_name, Key=key)
            return True
    
    async def list_files(self, prefix: Optional[str] = None, max_keys: int = 1000) -> List[Dict[str, Any]]:
        """
        List files in the R2 bucket
        
        Args:
            prefix: Optional prefix to filter files
            max_keys: Maximum number of keys to return
            
        Returns:
            List of file metadata dictionaries
        """
        session = self._get_session()
        async with session.client('s3', endpoint_url=self.endpoint_url, config=self.config) as s3:
            params = {
                'Bucket': self.bucket_name,
                'MaxKeys': max_keys
            }
            if prefix:
                params['Prefix'] = prefix
            
            response = await s3.list_objects_v2(**params)
            return response.get('Contents', [])


class CloudflareClient:
    """Main Cloudflare client that aggregates all services"""
    
    _d1_instance: Optional[CloudflareD1Client] = None
    _kv_instance: Optional[CloudflareKVClient] = None
    _r2_instance: Optional[CloudflareR2Client] = None
    
    @classmethod
    def get_d1_client(cls) -> Optional[CloudflareD1Client]:
        """Get D1 database client instance"""
        if not settings.cloudflare_d1_configured:
            return None
        
        if cls._d1_instance is None:
            cls._d1_instance = CloudflareD1Client(
                settings.cloudflare_account_id,
                settings.cloudflare_api_token,
                settings.cloudflare_d1_database_id
            )
        
        return cls._d1_instance
    
    @classmethod
    def get_kv_client(cls) -> Optional[CloudflareKVClient]:
        """Get KV storage client instance"""
        if not settings.cloudflare_kv_namespace_id:
            return None
        
        if cls._kv_instance is None:
            cls._kv_instance = CloudflareKVClient(
                settings.cloudflare_account_id,
                settings.cloudflare_api_token,
                settings.cloudflare_kv_namespace_id
            )
        
        return cls._kv_instance
    
    @classmethod
    def get_r2_client(cls) -> Optional[CloudflareR2Client]:
        """Get R2 object storage client instance"""
        if not settings.cloudflare_r2_configured:
            return None
        
        if cls._r2_instance is None:
            cls._r2_instance = CloudflareR2Client(
                settings.cloudflare_r2_account_id,
                settings.cloudflare_r2_access_key_id,
                settings.cloudflare_r2_secret_access_key,
                settings.cloudflare_r2_bucket_name
            )
        
        return cls._r2_instance


# Helper functions
def get_d1_client() -> Optional[CloudflareD1Client]:
    """Get Cloudflare D1 database client"""
    return CloudflareClient.get_d1_client()


def get_kv_client() -> Optional[CloudflareKVClient]:
    """Get Cloudflare KV storage client"""
    return CloudflareClient.get_kv_client()


def get_r2_client() -> Optional[CloudflareR2Client]:
    """Get Cloudflare R2 object storage client"""
    return CloudflareClient.get_r2_client()

