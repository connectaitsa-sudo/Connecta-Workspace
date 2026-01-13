"""Run script for the backend server"""

import uvicorn
from app.core.config import settings

if __name__ == "__main__":
    print(f"""
    ╔══════════════════════════════════════════════════════════╗
    ║  🎙️  AI Meeting Minutes System - Backend Server        ║
    ╚══════════════════════════════════════════════════════════╝
    
    Server starting on: http://{settings.HOST}:{settings.PORT}
    API Documentation: http://localhost:{settings.PORT}/docs
    """)
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
