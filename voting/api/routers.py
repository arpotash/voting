import fastapi
from fastapi.responses import JSONResponse
from voting import schemas
from voting.utils.vote import Vote

VOTING_ROUTER = fastapi.APIRouter(prefix="/voting-v1", tags=["voting"])


@VOTING_ROUTER.post("/create-topic")
async def create_voting_topic(
    voting_create_schema: schemas.VotingCreateSchema, request: fastapi.Request
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


@VOTING_ROUTER.post("/vote")
async def vote(voting_schema: schemas.VotingSchema, request: fastapi.Request) -> JSONResponse:
    """Vote for one of the answers"""
    vote_instance = Vote(request.app.state.redis)
    await vote_instance.vote(voting_schema.topic_uuid, voting_schema.answer)
    return JSONResponse(
        status_code=fastapi.status.HTTP_201_CREATED,
        content={"message": "The vote counted"},
    )


@VOTING_ROUTER.get("/results")
async def get_results_voting(topic: str, request: fastapi.Request) -> dict:
    """Get results of the voting by topic"""
    vote_instance = Vote(request.app.state.redis)
    results = await vote_instance.get_results(topic)
    return results
