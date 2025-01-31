from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class JournalEntryBase(BaseModel):
    entry_text: str

class JournalEntryCreate(JournalEntryBase):
    pass

class JournalEntry(JournalEntryBase):
    id: int
    sentiment_score: float
    mood: str
    ai_reflection: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class HabitBase(BaseModel):
    habit_name: str
    frequency: str  # daily, weekly, monthly

class HabitCreate(HabitBase):
    pass

class Habit(HabitBase):
    id: int
    streak: int
    created_at: datetime
    last_logged: Optional[datetime] = None

    class Config:
        from_attributes = True
