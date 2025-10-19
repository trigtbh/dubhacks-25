"""
Development server runner
Run this file directly to start the FastAPI server
"""

from dotenv import load_dotenv
load_dotenv()

import uvicorn
from app.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
        log_level="info"
    )

