"""Module containing interview questions data and related types."""
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel

class QuestionType(str, Enum):
    """Enum for different types of questions."""
    EXPLANATORY = "EXPLANATORY"
    TRUE_OR_FALSE = "TRUE_OR_FALSE"

class CommandType(str, Enum):
    """Enum for different command types."""
    ASK_QUESTION = "ASK_QUESTION"
    END_INTERVIEW = "END_INTERVIEW"

class Question(BaseModel):
    """Model representing an interview question."""
    command: CommandType
    type: Optional[QuestionType] = None
    question: Optional[str] = None

# In-memory questions list
QUESTIONS: List[Question] = [
    Question(
        command=CommandType.ASK_QUESTION,
        type=QuestionType.EXPLANATORY,
        question="Introduce yourself briefly please"
    ),
    Question(
        command=CommandType.ASK_QUESTION,
        type=QuestionType.EXPLANATORY,
        question="What are some of the difficult projects you've handled?"
    ),
    Question(
        command=CommandType.END_INTERVIEW
    )
]