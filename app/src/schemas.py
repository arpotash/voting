from typing import List

from pydantic import BaseModel, fields


class Option(BaseModel):
    name: str = fields.Field(example="Yes")
    count: int = fields.Field(description="votes count", example=12, default=0)


class VotingCreateSchema(BaseModel):
    topic: str = fields.Field(
        description="Topic of the voting",
        example="Rescheduling classes for next week",
    )
    options: List[Option] = fields.Field(
        description="Voting options",
        example=[
            {"name": "option1", "count": 0},
            {"name": "option2", "count": 0},
        ],
    )


class VotingSchema(BaseModel):
    topic_uuid: str = fields.Field(
        example="7405949021234727741"
    )
    answer: str = fields.Field(example="option1")
