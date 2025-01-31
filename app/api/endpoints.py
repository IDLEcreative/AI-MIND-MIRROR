from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import JournalEntry, Habit
from app.schemas.schemas import JournalEntryCreate, JournalEntry as JournalEntrySchema
from app.schemas.schemas import HabitCreate, Habit as HabitSchema
from textblob import TextBlob
import openai
from app.core.config import get_settings
from typing import List
import datetime

router = APIRouter()
settings = get_settings()

@router.post("/journal/", response_model=JournalEntrySchema)
def create_journal_entry(entry: JournalEntryCreate, db: Session = Depends(get_db)):
    # Analyze sentiment
    sentiment = TextBlob(entry.entry_text).sentiment.polarity
    mood = "Positive" if sentiment > 0 else "Negative" if sentiment < 0 else "Neutral"
    
    db_entry = JournalEntry(
        entry_text=entry.entry_text,
        sentiment_score=sentiment,
        mood=mood
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

@router.get("/journal/", response_model=List[JournalEntrySchema])
def get_journal_entries(db: Session = Depends(get_db)):
    return db.query(JournalEntry).all()

@router.post("/habits/", response_model=HabitSchema)
def create_habit(habit: HabitCreate, db: Session = Depends(get_db)):
    db_habit = Habit(
        habit_name=habit.habit_name,
        frequency=habit.frequency,
        last_logged=datetime.datetime.utcnow()
    )
    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)
    return db_habit

@router.get("/habits/", response_model=List[HabitSchema])
def get_habits(db: Session = Depends(get_db)):
    return db.query(Habit).all()

@router.post("/journal/analyze/")
async def analyze_journal(entry: JournalEntryCreate, db: Session = Depends(get_db)):
    if not settings.OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")
    
    openai.api_key = settings.OPENAI_API_KEY
    
    # Generate AI insights
    response = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI mentor helping users reflect on their thoughts."},
            {"role": "user", "content": f"Here is my journal entry: {entry.entry_text}. Can you give me feedback?"}
        ]
    )
    
    ai_feedback = response.choices[0].message.content
    
    # Save to database with sentiment and AI feedback
    sentiment = TextBlob(entry.entry_text).sentiment.polarity
    mood = "Positive" if sentiment > 0 else "Negative" if sentiment < 0 else "Neutral"
    
    db_entry = JournalEntry(
        entry_text=entry.entry_text,
        sentiment_score=sentiment,
        mood=mood,
        ai_reflection=ai_feedback
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    
    return {
        "entry": db_entry,
        "ai_feedback": ai_feedback,
        "mood": mood
    }
