from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from app.config import settings
from app.api import routes
from app.api import cloudflare_routes

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

# Include API routes
app.include_router(routes.router)
app.include_router(cloudflare_routes.router)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Unfreeze API is running",
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "environment": settings.environment
    }

@app.get("/health")
async def health_check():
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
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True if settings.environment == "development" else False
    )
