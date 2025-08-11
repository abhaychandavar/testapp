"""API endpoints for managing interview questions."""
from fastapi import APIRouter, Depends
from redis import Redis
from app.core.questions import Question
from app.core.models import AnswerRequest, ValidationResponse
from app.services.question_service import QuestionService
from app.services.validation_service import ValidationService

router = APIRouter()

async def get_redis() -> Redis:
    """Get Redis client instance.
    
    Returns:
        Redis client instance
    """
    from app.core.redis import get_redis_client
    return await get_redis_client()

def get_question_service(redis: Redis = Depends(get_redis)) -> QuestionService:
    """Get QuestionService instance.
    
    Args:
        redis: Redis client instance
        
    Returns:
        QuestionService instance
    """
    return QuestionService(redis)

def get_validation_service(redis: Redis = Depends(get_redis)) -> ValidationService:
    """Get ValidationService instance.
    
    Args:
        redis: Redis client instance
        
    Returns:
        ValidationService instance
    """
    return ValidationService(redis)

@router.get("/next/{session_id}", response_model=Question)
async def get_next_question(
    session_id: str,
    question_service: QuestionService = Depends(get_question_service)
) -> Question:
    """Get next question for a session.
    
    Args:
        session_id: Unique identifier for the interview session
        question_service: Service for managing questions
        
    Returns:
        Question object with format:
        {
            command: "ASK_QUESTION" | "END_INTERVIEW",
            type: "EXPLANATORY" | "TRUE_OR_FALSE" | null,
            question: string | null
        }
    """
    return await question_service.get_next_question(session_id)

@router.post("/validate/{session_id}", response_model=ValidationResponse)
async def validate_answer(
    session_id: str,
    answer_request: AnswerRequest,
    validation_service: ValidationService = Depends(get_validation_service)
) -> ValidationResponse:
    """Validate an answer for the current question.
    
    Args:
        session_id: Unique identifier for the interview session
        answer_request: The answer to validate
        validation_service: Service for validating answers
        
    Returns:
        Validation response with format:
        {
            followupQuestion: string | null,
            proceedToNextQuestion: boolean
        }
    """
    return await validation_service.validate_answer(session_id, answer_request.answer)