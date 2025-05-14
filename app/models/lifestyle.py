from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class LifestyleEntry(BaseModel):
    id: str
    user_id: str
    date: datetime
    foods_consumed: List[str]
    potential_trigger_foods: List[str]
    sleep_hours: int
    stress_level: int
    water_intake_liters: float
    exercise_minutes: int
    notes: Optional[List[str]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
