from beartype.typing import List
from pydantic import BaseModel, Field


def ArxivDict(BaseModel):
    """ArxivDict model."""
    link: dict = {}
    published: datetime


# def SequenceArxivDict() -> List[ArxivDict]:
#     """SequenceArxivDict model."""
#     List[ArxivDict] = Field(default_factory=list)
