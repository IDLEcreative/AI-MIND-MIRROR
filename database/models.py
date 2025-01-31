from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    journal_entries = relationship("JournalEntry", back_populates="user")
    habits = relationship("Habit", back_populates="user")
    check_ins = relationship("CheckIn", back_populates="user")

class JournalEntry(Base):
    __tablename__ = "journal_entries"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    entry_text = Column(String)
    sentiment_score = Column(Float)
    mood = Column(String)
    ai_reflection = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="journal_entries")

class Habit(Base):
    __tablename__ = "habits"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    habit_name = Column(String)
    frequency = Column(String)  # daily, weekly, monthly
    streak = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_logged = Column(DateTime)
    
    # Relationship
    user = relationship("User", back_populates="habits")

class CheckIn(Base):
    __tablename__ = "check_ins"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    mood = Column(Integer)  # 1-10 scale
    energy = Column(Integer)  # 1-10 scale
    stress = Column(Integer)  # 1-10 scale
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="check_ins")
