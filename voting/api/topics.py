import fastapi
from voting import schemas
from voting.utils.vote import Vote

TOPIC_ROUTER = fastapi.APIRouter(prefix="/voting-v1", tags=["topics"])


@TOPIC_ROUTER.post("/create-topic")
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


@TOPIC_ROUTER.get("/{topic_id}/votes")
async def get_results_voting(topic_id: str, request: fastapi.Request) -> dict:
    """Get results of the voting by topic"""
    vote_instance = Vote(request.app.state.redis)
    results = await vote_instance.get_results(topic_id)
    return results
