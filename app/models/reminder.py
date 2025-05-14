from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Reminder(BaseModel):
    id: str
    user_id: str
    title: str
    description: Optional[str] = None
    reminder_type: Optional[str] = None
    date_time: datetime
    repeat_days: List[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
