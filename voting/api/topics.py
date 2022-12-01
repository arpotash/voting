import fastapi
from voting import schemas
from voting.services.vote import Topic

TOPIC_ROUTER = fastapi.APIRouter(prefix="/voting-v1", tags=["topics"])


@TOPIC_ROUTER.post("/topics")
async def create_voting_topic(
    voting_create_schema: schemas.VotingCreateSchema, request: fastapi.Request
) -> str:
    """Create voting topic with some answer options"""
    vote_instance = Topic(request.app.state.redis)
    options = {
        option.name: option.count for option in voting_create_schema.options
    }
    voting_topic_id = await vote_instance.create_topic(
        voting_create_schema.topic, options
    )
    return voting_topic_id
