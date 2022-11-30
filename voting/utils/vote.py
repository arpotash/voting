import json
import fastapi

from voting.core.config import settings
from voting.core.logger import get_logger
from voting.utils.redis import RedisClient

LOGGER = get_logger("utils")


class Vote:
    def __init__(self, cache: RedisClient):
        self.cache = cache

    async def create_topic(self, name: str, answers: dict) -> str:
        """Create topic and set it to redis with some answer options as a nested dictionary"""
        voting_topic_id = str(hash(name))
        await self.cache.set(
            voting_topic_id,
            json.dumps(answers),
            ex=settings.redis_expiration_time,
        )
        return voting_topic_id

    async def vote(self, topic_id: str, answer: str) -> None:
        """Check topic, answer and vote for the answer if it exists"""
        try:
            answer_dict = (await self.cache.get(topic_id)).decode("utf-8")
            answers_json = json.loads(answer_dict)
            if answers_json.get(answer, None) is None:
                raise fastapi.HTTPException(
                    status_code=fastapi.status.HTTP_400_BAD_REQUEST,
                    detail={"error": "Incorrect answer"},
                )
            answers_json[answer] += 1
            await self.cache.set(
                topic_id,
                json.dumps(answers_json),
                ex=settings.redis_expiration_time,
            )
        except AttributeError as e:
            LOGGER.error(e)
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail={"error": "Topic not found"},
            )

    async def get_results(self, topic: str) -> dict:
        """Get statistic of the voting by answers in percents"""
        results_by_percents = {}
        voting_results = await self.cache.get(topic)
        try:
            votes_by_answer = json.loads(
                voting_results.decode("utf-8")
            ).items()
        except AttributeError as e:
            LOGGER.error(e)
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail={"error": "Topic not found"},
            )
        count_answers = sum([value for key, value in votes_by_answer])
        for answer, votes in votes_by_answer:
            results_by_percents[answer] = float(
                "{percent:.2f}".format(percent=votes / count_answers * 100)
            )
        return results_by_percents
