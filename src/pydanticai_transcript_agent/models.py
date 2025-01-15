from pydantic import BaseModel, Field
from typing import List, Optional

class Transcript(BaseModel):
    """Model for a transcript."""
    text: str = Field(..., description="The full text of the transcript")

class IdeaItem(BaseModel):
    """Individual content idea with metadata."""
    idea: str = Field(description="Title of the idea")
    category: str = Field(description="Category of the idea")
    engagement: int = Field(description="Engagement score (1-5)", ge=1, le=5)
    mentioned_by: Optional[str] = Field(description="Who mentioned this idea", default=None)
    summary: str = Field(description="Detailed summary of the idea", default=None)
