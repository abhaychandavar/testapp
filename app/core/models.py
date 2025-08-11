"""Models for request/response data structures."""
from typing import Optional
from pydantic import BaseModel

class AnswerRequest(BaseModel):
    """Request model for answer validation."""
    answer: str

class ValidationResponse(BaseModel):
    """Response model for answer validation."""
    followupQuestion: Optional[str] = None
    proceedToNextQuestion: bool
