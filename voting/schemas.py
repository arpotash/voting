import typing
import pydantic


class Option(pydantic.BaseModel):
    name: str = pydantic.fields.Field(example="Yes")
    count: int = pydantic.fields.Field(description="votes count", example=12, default=0)


class VotingCreateSchema(pydantic.BaseModel):
    topic: str = pydantic.fields.Field(
        description="Topic of the voting",
        example="Rescheduling classes for next week",
    )
    options: typing.List[Option] = pydantic.fields.Field(
        description="Voting options",
        example=[
            {"name": "option1", "count": 0},
            {"name": "option2", "count": 0},
        ],
    )


class VotingSchema(pydantic.BaseModel):
    answer: str = pydantic.fields.Field(example="option1")
