from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class SymptomEntry(BaseModel):
    id: str
    user_id: str
    date: datetime
    is_flareup: bool
    severity: str
    affected_areas: List[str]
    symptoms: Optional[List[str]] = None
    medications: Optional[List[str]] = None
    notes: Optional[List[str]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

