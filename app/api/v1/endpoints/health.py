from fastapi import APIRouter
from app.core.config import settings
from app.core.redis import RedisClient
from datetime import datetime

router = APIRouter()

@router.get("/health")
async def health_check():
    """
    Health check endpoint that returns the status of the application
    and its dependencies.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.VERSION,
        "environment": settings.ENV
    }

@router.get("/health/detailed")
async def detailed_health_check():
    """
    Detailed health check that includes the status of all dependencies
    like Redis, cache, etc.
    """
    redis_client = RedisClient()
    redis_status = "healthy"
    redis_error = None
    
    try:
        # Try to ping Redis
        await redis_client.set("health_check", "ok", expire_seconds=5)
        await redis_client.get("health_check")
    except Exception as e:
        redis_status = "unhealthy"
        redis_error = str(e)
    
    checks = {
        "api": {
            "status": "healthy",
            "version": settings.VERSION,
            "environment": settings.ENV
        },
        "redis": {
            "status": redis_status,
            "error": redis_error,
            "host": settings.REDIS_HOST,
            "port": settings.REDIS_PORT
        }
    }
    
    overall_status = all(
        check.get("status") == "healthy" 
        for check in checks.values()
    )
    
    return {
        "status": "healthy" if overall_status else "unhealthy",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": checks
    }
