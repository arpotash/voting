from fastapi import FastAPI

from app.src.routers import voting_router
from app.utils.redis import RedisClient

app = FastAPI()
app.include_router(voting_router)


@app.on_event("startup")
async def startup_event() -> None:
    """Redis init after running the application"""
    redis_client = RedisClient()
    await redis_client.redis_connect()
    app.state.redis = redis_client


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Redis connection closing after finishing the application"""
    await app.state.redis._close()
