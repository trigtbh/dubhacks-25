"""
Cloudflare D1 Database and Services Client

This client provides access to Cloudflare services while running on Oracle Cloud:
- D1 Database (SQLite-compatible)
- KV (Key-Value storage)
- R2 (Object storage)
"""

from typing import Optional, Any, Dict, List
import httpx
from app.config import settings

class CloudflareD1Client:
    """
    Cloudflare D1 Database client for REST API access
    
    Usage:
        client = get_d1_client()
        if client:
            # Execute query
            result = await client.query("SELECT * FROM users WHERE id = ?", [user_id])
            
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


class CloudflareClient:
    """Main Cloudflare client that aggregates all services"""
    
    _d1_instance: Optional[CloudflareD1Client] = None
    _kv_instance: Optional[CloudflareKVClient] = None
    
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


# Helper functions
def get_d1_client() -> Optional[CloudflareD1Client]:
    """Get Cloudflare D1 database client"""
    return CloudflareClient.get_d1_client()


def get_kv_client() -> Optional[CloudflareKVClient]:
    """Get Cloudflare KV storage client"""
    return CloudflareClient.get_kv_client()

