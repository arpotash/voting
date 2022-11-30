from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

from app.core.logger import get_logger
from app.src.schemas import VotingCreateSchema, VotingSchema
from app.utils.vote import Vote

voting_router = APIRouter(prefix="/api-v1", tags=["voting"])
logger = get_logger("voting")


@voting_router.post("/create-topic")
async def create_voting_topic(
    voting_create_schema: VotingCreateSchema, request: Request
) -> str:
    """Create voting topic with some answer options"""
    vote_instance = Vote(request.app.state.redis)
    options = {
        option.name: option.count for option in voting_create_schema.options
    }
    voting_topic_id = await vote_instance.create_topic(
        voting_create_schema.topic, options
    )
    return voting_topic_id


@voting_router.post("/vote")
async def vote(voting_schema: VotingSchema, request: Request) -> JSONResponse:
    """Vote for one of the answers"""
    vote_instance = Vote(request.app.state.redis)
    await vote_instance.vote(voting_schema.topic_uuid, voting_schema.answer)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "The vote counted"},
    )


@voting_router.get("/results")
async def get_results_voting(topic: str, request: Request) -> dict:
    """Get results of the voting by topic"""
    vote_instance = Vote(request.app.state.redis)
    results = await vote_instance.get_results(topic)
    return results
