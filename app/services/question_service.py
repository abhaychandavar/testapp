"""Service for managing interview questions using Redis."""
from typing import Optional
from redis import Redis
from app.core.questions import Question, QUESTIONS
from app.core.redis_keys import get_current_question_idx_key

class QuestionService:
    """Service for managing interview questions."""
    
    def __init__(self, redis_client: Redis):
        """Initialize the service with Redis client.
        
        Args:
            redis_client: Redis client instance
        """
        self.redis = redis_client

    async def get_next_question(self, session_id: str) -> Question:
        """Get the next question for a given session.
        
        Args:
            session_id: Unique identifier for the interview session
            
        Returns:
            Next question for the session
        """
        # Get current question index from Redis
        curr_idx_key = get_current_question_idx_key(session_id)
        curr_idx_raw = await self.redis.get(curr_idx_key)
        curr_idx = int(curr_idx_raw) if curr_idx_raw else 0
        
        # Get the question
        question = QUESTIONS[curr_idx]
        
        # Increment the index for next time
        next_idx = curr_idx + 1
        if next_idx < len(QUESTIONS):
            await self.redis.set(curr_idx_key, str(next_idx))
            
        return question
