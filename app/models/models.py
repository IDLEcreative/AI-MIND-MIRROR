from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
import datetime

class JournalEntry(Base):
    __tablename__ = "journal_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    entry_text = Column(String)
    sentiment_score = Column(Float)
    mood = Column(String)
    ai_reflection = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Habit(Base):
    __tablename__ = "habits"
    
    id = Column(Integer, primary_key=True, index=True)
    habit_name = Column(String)
    frequency = Column(String)  # daily, weekly, monthly
    streak = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_logged = Column(DateTime)
