import os
from typing import Optional
from pydantic import BaseModel


class Settings(BaseModel):
    app_host: str = os.getenv("APP_HOST", "127.0.0.1")
    app_port: int = int(os.getenv("APP_PORT", "8000"))
    redis_host: str = os.getenv("REDIS_HOST", "127.0.0.1")
    redis_port: str = os.getenv("REDIS_PORT", "6379")
    redis_expiration_time: Optional[float] = int(
        os.getenv("REDIS_EXPIRATION_TIME", 15)
    )


settings = Settings()
