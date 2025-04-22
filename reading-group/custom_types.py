from beartype.typing import List
from pydantic import BaseModel, Field


def ArxivDict(BaseModel):
    """ArxivDict model."""
    title: str
    summary: str
    link: str
    published: datetime


# def SequenceArxivDict() -> List[ArxivDict]:
#     """SequenceArxivDict model."""
#     List[ArxivDict] = Field(default_factory=list)
