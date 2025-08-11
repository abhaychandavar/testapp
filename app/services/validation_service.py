"""Service for validating interview answers."""
from redis import Redis
from app.core.models import ValidationResponse
from app.core.redis_keys import get_current_question_idx_key, REDIS_KEY_EXPIRATION

class ValidationService:
    """Service for validating interview answers."""
    
    def __init__(self, redis_client: Redis):
        """Initialize the service with Redis client.
        
        Args:
            redis_client: Redis client instance
        """
        self.redis = redis_client

    async def validate_answer(self, session_id: str, answer: str) -> ValidationResponse:
        """Validate an answer and update the question index.
        
        Args:
            session_id: Unique identifier for the interview session
            answer: The answer provided by the interviewee
            
        Returns:
            ValidationResponse with followup question (if any) and whether to proceed
        """
        # Get current question index
        curr_idx_key = get_current_question_idx_key(session_id)
        curr_idx_raw = await self.redis.get(curr_idx_key)
        curr_idx = int(curr_idx_raw) if curr_idx_raw else 0
        
        # Log the answer (you can extend this for more sophisticated validation)
        print(f"Question IDX {curr_idx}, answer: {answer}")
        
        # Increment and store the index with expiration
        next_idx = curr_idx + 1
        await self.redis.set(
            curr_idx_key,
            str(next_idx),
            ex=REDIS_KEY_EXPIRATION  # 3 hours expiration
        )
        
        # For now, always proceed to next question without followup
        return ValidationResponse(
            followupQuestion=None,
            proceedToNextQuestion=True
        )
