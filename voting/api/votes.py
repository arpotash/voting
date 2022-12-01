import fastapi
from fastapi.responses import JSONResponse
from voting import schemas
from voting.services.vote import Vote

VOTING_ROUTER = fastapi.APIRouter(prefix="/voting-v1", tags=["votes"])


@VOTING_ROUTER.put("/topics/{topic_id}/votes")
async def vote(topic_id: str, voting_schema: schemas.VotingSchema, request: fastapi.Request) -> JSONResponse:
    """Vote for one of the answers"""
    vote_instance = Vote(request.app.state.redis)
    await vote_instance.vote(topic_id, voting_schema.answer)
    return JSONResponse(
        status_code=fastapi.status.HTTP_201_CREATED,
        content={"message": "The vote counted"},
    )


@VOTING_ROUTER.get("/topics/{topic_id}/votes")
async def get_results_voting(topic_id: str, request: fastapi.Request) -> dict:
    """Get results of the voting by topic"""
    vote_instance = Vote(request.app.state.redis)
    results = await vote_instance.get_results(topic_id)
    return results
