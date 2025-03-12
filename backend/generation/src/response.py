from typing import List, Union
from pydantic import BaseModel, Field

class BulletPoint(BaseModel):
    text: str = Field(description="The text of the bullet point")
    subpoints: List["BulletPoint"] = Field(description="Subpoints of the bullet point", 
                                           default_factory=list)

class ContentBlock(BaseModel):
    content: Union[str, List[BulletPoint]] = Field(
        description="A block of content, can be a string or a combination of a string and a list of bullet points",
    )

class Response(BaseModel):
    response: List[ContentBlock] = Field(
        description="The response to the query. Structured with short sentences and bullet points.",
    )