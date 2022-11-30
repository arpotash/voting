import os
from typing import Optional

from pydantic import BaseModel


class Settings(BaseModel):
    redis_host: str = os.getenv("REDIS_HOST", "127.0.0.1")
    redis_port: str = os.getenv("REDIS_PORT", "6379")
    redis_expiration_time: Optional[float] = int(
        os.getenv("REDIS_EXPIRATION_TIME", 15)
    )


settings = Settings()
