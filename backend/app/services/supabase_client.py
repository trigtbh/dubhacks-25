from typing import Optional
from supabase import create_client, Client
from app.config import settings

class SupabaseClient:
    """
    Supabase client wrapper for database operations
    
    Usage:
        1. Set up your Supabase project at https://supabase.com
        2. Add your SUPABASE_URL and SUPABASE_KEY to .env file
        3. Use this client to interact with your database
    
    Example:
        supabase = get_supabase_client()
        if supabase:
            # Query data
            response = supabase.table('users').select("*").execute()
            
            # Insert data
            data = supabase.table('users').insert({"name": "John"}).execute()
            
            # Update data
            supabase.table('users').update({"name": "Jane"}).eq('id', 1).execute()
    """
    
    _instance: Optional[Client] = None
    
    @classmethod
    def get_client(cls) -> Optional[Client]:
        """
        Get or create Supabase client instance
        Returns None if Supabase is not configured
        """
        if not settings.supabase_configured:
            return None
            
        if cls._instance is None:
            cls._instance = create_client(
                settings.supabase_url,
                settings.supabase_key
            )
        
        return cls._instance
    
    @classmethod
    def is_configured(cls) -> bool:
        """Check if Supabase is properly configured"""
        return settings.supabase_configured

def get_supabase_client() -> Optional[Client]:
    """Helper function to get Supabase client"""
    return SupabaseClient.get_client()

