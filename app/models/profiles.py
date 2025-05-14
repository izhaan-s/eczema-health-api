from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Profile(BaseModel):
    id: str
    email: str
    display_name: str
    first_name: str
    last_name: str
    avatar_url: Optional[str] = None
    date_of_birth: datetime
    known_allergies: Optional[List[str]] = None
    medical_notes: Optional[List[str]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
