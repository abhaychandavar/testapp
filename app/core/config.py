from typing import List, Union
from enum import Enum
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, field_validator
import os
from dotenv import load_dotenv
from functools import lru_cache

# Load environment variables from .env file
load_dotenv()

class EnvironmentType(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

class Settings(BaseSettings):
    # Project metadata
    PROJECT_NAME: str = "Interview Orchestrator"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "API for orchestrating and managing interviews"
    
    # API configuration
    API_V1_STR: str = "/api/v1"
    
    # Environment
    ENV: EnvironmentType = EnvironmentType.DEVELOPMENT
    DEBUG: bool = False
    
    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"
    
    # CORS
    ALLOWED_ORIGINS: List[Union[str, AnyHttpUrl]] = []
    
    # Redis Configuration
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "")
    REDIS_USERNAME: str = os.getenv("REDIS_USERNAME", "")
    REDIS_USE_SSL: bool = os.getenv("REDIS_USE_SSL", "False").lower() == "true"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    @field_validator("ALLOWED_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    @property
    def redis_url(self) -> str:
        """Build Redis URL from components."""
        scheme = "rediss" if self.REDIS_USE_SSL else "redis"
        auth = ""
        if self.REDIS_USERNAME and self.REDIS_PASSWORD:
            auth = f"{self.REDIS_USERNAME}:{self.REDIS_PASSWORD}@"
        url = f"{scheme}://{auth}{self.REDIS_HOST}:{self.REDIS_PORT}"
        print("URL <><>", url)
        return url
    
    class Config:
        case_sensitive = True
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()

# Create settings instance
settings = get_settings()
