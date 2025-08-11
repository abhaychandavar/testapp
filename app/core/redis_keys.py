"""Helper module for managing Redis keys consistently across the application."""
from typing import Final

# Key prefixes
INTERVIEW_PREFIX: Final[str] = "interview"
QUESTION_PREFIX: Final[str] = "question"

# Redis key expiration time in seconds (3 hours)
REDIS_KEY_EXPIRATION: Final[int] = 10800

def get_current_question_idx_key(session_id: str) -> str:
    """Generate Redis key for storing current question index for a session.
    
    Args:
        session_id: Unique identifier for the interview session
        
    Returns:
        Formatted Redis key string
    """
    return f"{INTERVIEW_PREFIX}:{session_id}:{QUESTION_PREFIX}:idx"