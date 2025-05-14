from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PhotoEntry(BaseModel):
    id: str
    user_id: str
    image_url: str
    body_part: str
    itch_intensity: int
    notes: Optional[List[str]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
