from datetime import datetime

from beartype.typing import List
from pydantic import BaseModel, Field


class ArxivDict(BaseModel):
    """ArxivDict model."""
    link: dict = {}
    published: datetime


# def SequenceArxivDict() -> List[ArxivDict]:
#     """SequenceArxivDict model."""
#     List[ArxivDict] = Field(default_factory=list)
