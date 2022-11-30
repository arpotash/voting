import fastapi
from fastapi.responses import JSONResponse
from voting import schemas
from voting.utils.vote import Vote

VOTING_ROUTER = fastapi.APIRouter(prefix="/voting-v1", tags=["votes"])


@VOTING_ROUTER.post("/{topic_id}/votes")
async def vote(topic_id: str, voting_schema: schemas.VotingSchema, request: fastapi.Request) -> JSONResponse:
    """Vote for one of the answers"""
    vote_instance = Vote(request.app.state.redis)
    await vote_instance.vote(topic_id, voting_schema.answer)
    return JSONResponse(
        status_code=fastapi.status.HTTP_201_CREATED,
        content={"message": "The vote counted"},
    )
