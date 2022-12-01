import typing
import aioredis

from voting.settings import settings
from voting.logger import get_logger

logger = get_logger("utils")


class RedisClient:
    def __init__(self) -> None:
        """Initializes redis client"""
        self._redis_cli: typing.Optional[aioredis.Redis] = None

    async def redis_connect(self) -> None:
        try:
            self._redis_cli = aioredis.from_url(
                f"redis://{settings.redis_host}:{settings.redis_port}",
                decode_responses=True
            )
        except ConnectionError as e:
            logger.error("Service is unavailable")

    async def set(
        self, key: str, value: str, ex: typing.Optional[int] = None
    ) -> None:
        """Set a new value to cash
        :param key: cache key
        :param value: cache value
        :param ex: cache lifetime
        """
        await self._redis_cli.set(key, value, ex=ex)

    async def get(self, key: str) -> typing.Any:
        """Get value by key"""
        return await self._redis_cli.get(key)

    async def close(self) -> None:
        """Close the connection"""
        await self._redis_cli.close()
