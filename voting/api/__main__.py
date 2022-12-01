import uvicorn
from fastapi import FastAPI
from voting.settings import settings
from voting.api.votes import VOTING_ROUTER
from voting.api.topics import TOPIC_ROUTER
from voting.resources.redis import RedisClient

app = FastAPI()
app.include_router(VOTING_ROUTER)
app.include_router(TOPIC_ROUTER)


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


if __name__ == "__main__":
    uvicorn.run(app, host=settings.app_host, port=settings.app_port)
