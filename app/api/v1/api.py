from fastapi import APIRouter
from app.api.v1.endpoints import health, questions

api_router = APIRouter()

# Include routers
api_router.include_router(health.router, tags=["health"])
api_router.include_router(questions.router, prefix="/questions", tags=["questions"])
