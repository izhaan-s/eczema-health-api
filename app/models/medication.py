from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Medication(BaseModel):
    id: str
    user_id: str
    name: str
    dosage: str
    frequency: str
    start_date: datetime
    end_date: Optional[datetime] = None
    effectiveness: Optional[int] = None
    side_effects: Optional[List[str]] = None
    notes: Optional[List[str]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        
