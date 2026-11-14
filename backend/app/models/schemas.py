from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class AssistantMode(str, Enum):
    HEALTH = "health"
    EDUCATION = "education"


class ChatRequest(format := BaseModel):
    query: str = Field(..., description="The user's question or prompt.")
    mode: AssistantMode = Field(
        default=AssistantMode.HEALTH,
        description="Select whether to query Health Awareness or Learning Assistant mode.",
    )


class SourceCitation(BaseModel):
    title: str = Field(..., description="Title of the verified reference document or guideline.")
    category: str = Field(..., description="Category: 'health' or 'education'.")
    source_url: Optional[str] = Field(None, description="External reference link if available.")


class ChatResponse(BaseModel):
    mode: AssistantMode
    answer: str
    sources: List[SourceCitation] = []
    safety_disclaimer: Optional[str] = None