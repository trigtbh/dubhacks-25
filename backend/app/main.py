from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from app.config import settings
from app.api import routes
from app.api import supabase_routes

app = FastAPI(
    title="Unfreeze API",
    description="Backend API for the Unfreeze application",
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
app.include_router(supabase_routes.router)

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
        "services": {
            "api": "operational",
            "supabase": "not_configured" if not settings.supabase_url else "configured"
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

