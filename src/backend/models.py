from pydantic import BaseModel
from typing import List

class ExtractedEvent(BaseModel):
    date: str
    title: str
    context: str
    document: str

class ExtractedEventResponse(BaseModel):
    events: List[ExtractedEvent]
