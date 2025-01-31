from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """Base schema for user data."""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr

class UserCreate(UserBase):
    """Schema for user registration."""
    password: str = Field(..., min_length=8)

class JournalEntryCreate(BaseModel):
    """Schema for creating a journal entry."""
    entry_text: str = Field(..., min_length=1, max_length=5000)
    mood: Optional[str] = Field(None, max_length=50)
    tags: Optional[list[str]] = []

class HabitCreate(BaseModel):
    """Schema for creating a habit."""
    habit_name: str = Field(..., min_length=1, max_length=100)
    frequency: str = Field(..., pattern='^(daily|weekly|monthly)$')
    description: Optional[str] = Field(None, max_length=500)

class CheckInCreate(BaseModel):
    """Schema for creating a well-being check-in."""
    mood: int = Field(..., ge=1, le=10)
    energy: int = Field(..., ge=1, le=10)
    stress: int = Field(..., ge=1, le=10)
    notes: Optional[str] = Field(None, max_length=1000)

# Response Models
class JournalEntryResponse(JournalEntryCreate):
    """Schema for journal entry response."""
    id: int
    user_id: str
    created_at: datetime
    ai_insights: Optional[str]
    
    class Config:
        from_attributes = True

class HabitResponse(HabitCreate):
    """Schema for habit response."""
    id: int
    user_id: str
    streak: int
    created_at: datetime
    last_logged: Optional[datetime]
    
    class Config:
        from_attributes = True

class CheckInResponse(CheckInCreate):
    """Schema for check-in response."""
    id: int
    user_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True
