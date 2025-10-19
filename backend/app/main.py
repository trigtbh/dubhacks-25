from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request # New import for session helpers
from authlib.integrations.starlette_client import OAuth
from datetime import datetime
from app.config import settings
from app.api import routes
from app.api import cloudflare_routes
from app.api import vectorization_routes
from app.api import user_routes
from app.api import auth_routes
from app.api import challenge_routes
from app.dependencies import get_current_user


app = FastAPI(
    title="Unfreeze API",
    description="Backend API for the Unfreeze application - Running on Oracle Cloud with Cloudflare services",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Session Middleware for OAuth
app.add_middleware(SessionMiddleware, secret_key=settings.session_secret_key)

# Include API routes
app.include_router(routes.router)
app.include_router(cloudflare_routes.router)
app.include_router(vectorization_routes.router)
app.include_router(user_routes.router)
app.include_router(auth_routes.router)
app.include_router(challenge_routes.router)

@app.get("/")
async def root(current_user: dict = Depends(get_current_user)):
    """Health check endpoint"""
    return {
        "message": "Unfreeze API is running",
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "environment": settings.environment,
        "user": current_user
    }

@app.get("/health")
async def health_check(current_user: dict = Depends(get_current_user)):
    """Detailed health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "platform": {
            "hosting": "Oracle Cloud",
            "services": "Cloudflare (D1, KV)"
        },
        "services": {
            "api": "operational",
            "cloudflare_d1": "configured" if settings.cloudflare_d1_configured else "not_configured",
            "cloudflare_kv": "configured" if settings.cloudflare_kv_namespace_id else "not_configured"
        },
        "user": current_user
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True if settings.environment == "development" else False
    )
