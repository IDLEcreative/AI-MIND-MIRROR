from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from database.models import Base, JournalEntry, Habit, User
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
import os
import openai
from textblob import TextBlob
from pydantic import BaseModel
from typing import Optional, List

# Pydantic models for request/response
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class JournalEntryCreate(BaseModel):
    entry_text: str

class JournalEntryResponse(BaseModel):
    id: int
    entry_text: str
    sentiment_score: float
    mood: str
    ai_reflection: Optional[str]
    created_at: datetime

class HabitCreate(BaseModel):
    habit_name: str
    frequency: str

# Load environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://jamesguy@localhost/mindmirror")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Database setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize FastAPI
app = FastAPI(title="Mind Mirror API", description="AI-powered self-reflection & personal growth")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency Injection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API Endpoints
@app.get("/")
def read_root():
    return {"message": "Welcome to Mind Mirror API"}

@app.post("/users/", response_model=dict)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # In a real app, hash the password here
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=user.password  # Don't do this in production!
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully", "user_id": new_user.id}

@app.post("/journal/", response_model=JournalEntryResponse)
def add_journal_entry(entry: JournalEntryCreate, user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Analyze sentiment
    sentiment = TextBlob(entry.entry_text).sentiment.polarity
    mood = "Positive" if sentiment > 0 else "Negative" if sentiment < 0 else "Neutral"

    journal_entry = JournalEntry(
        user_id=user.id,
        entry_text=entry.entry_text,
        sentiment_score=sentiment,
        mood=mood
    )
    db.add(journal_entry)
    db.commit()
    db.refresh(journal_entry)
    
    return journal_entry

@app.get("/journal/{user_id}", response_model=List[JournalEntryResponse])
def get_journal_entries(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    entries = db.query(JournalEntry).filter(JournalEntry.user_id == user_id).all()
    return entries

@app.post("/habits/")
def track_habit(habit: HabitCreate, user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    habit_entry = Habit(
        user_id=user.id,
        habit_name=habit.habit_name,
        frequency=habit.frequency,
        last_logged=datetime.utcnow()
    )
    db.add(habit_entry)
    db.commit()
    return {"message": f"Habit '{habit.habit_name}' logged successfully."}

@app.post("/journal/analyze/")
def analyze_journal_entry(entry: JournalEntryCreate, user_id: int, db: Session = Depends(get_db)):
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")
    
    openai.api_key = OPENAI_API_KEY

    # Generate AI insights
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are an AI mentor helping users reflect on their thoughts."},
            {"role": "user", "content": f"Here is my journal entry: {entry_text}. Can you give me feedback?"}
        ]
    )

    ai_feedback = response.choices[0].message.content

    # Save to DB with sentiment analysis
    sentiment = TextBlob(entry_text).sentiment.polarity
    mood = "Positive" if sentiment > 0 else "Negative" if sentiment < 0 else "Neutral"
    
    journal_entry = JournalEntry(
        user_id=user_id,
        entry_text=entry_text,
        sentiment_score=sentiment,
        mood=mood,
        ai_reflection=ai_feedback
    )
    db.add(journal_entry)
    db.commit()

    return {"message": "Journal entry analyzed!", "feedback": ai_feedback, "mood": mood}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add authentication router
app.include_router(auth_router, prefix="/auth", tags=["authentication"])

# Security setup
API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key != settings.app_secret:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key"
        )
    return api_key

@app.post("/journal-entries/", response_model=JournalEntryResponse)
async def create_journal_entry(
    entry_data: JournalEntryCreate,
    current_user: str = Depends(get_current_user)
) -> JournalEntryResponse:
    """Create a new journal entry with AI-powered reflection."""
    try:
        # Get AI analysis
        reflection = await generate_ai_reflection(entry_data.entry_text)
        
        # Create journal entry
        journal_entry = {
            "user_id": current_user,
            "entry_text": entry_data.entry_text,
            "ai_insights": reflection,
            "created_at": datetime.utcnow()
        }
        
        return JournalEntryResponse(**journal_entry)
    except Exception as e:
        logger.error(f"Error creating journal entry: {str(e)}")
        raise handle_database_error(e)

@app.post("/habits/", response_model=HabitResponse)
async def create_habit(
    habit_data: HabitCreate,
    current_user: str = Depends(get_current_user)
) -> HabitResponse:
    """Create a new habit to track."""
    try:
        habit = {
            "user_id": current_user,
            "habit_name": habit_data.habit_name,
            "frequency": habit_data.frequency,
            "description": habit_data.description,
            "streak": 0,
            "created_at": datetime.utcnow()
        }
        
        return HabitResponse(**habit)
    except Exception as e:
        logger.error(f"Error creating habit: {str(e)}")
        raise handle_database_error(e)

@app.post("/check-ins/", response_model=CheckInResponse)
async def create_check_in(
    check_in_data: CheckInCreate,
    current_user: str = Depends(get_current_user)
) -> CheckInResponse:
    """Create a new well-being check-in."""
    try:
        check_in = {
            "user_id": current_user,
            **check_in_data.dict(),
            "created_at": datetime.utcnow()
        }
        
        return CheckInResponse(**check_in)
    except Exception as e:
        logger.error(f"Error creating check-in: {str(e)}")
        raise handle_database_error(e)

@app.post("/reflection/", status_code=status.HTTP_201_CREATED)
async def create_reflection(
    reflection_data: str,
    current_user: str = Depends(get_current_user)
):
    try:
        # Get AI analysis
        agent = ReflectionAgent(user_input=reflection_data)
        result = agent.run()
        
        return {
            "message": "Reflection created with AI insights",
            "insights": result
        }
    
    except Exception as e:
        logger.error(f"Error creating reflection: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing reflection"
        )

@app.post("/habit-tracking/", status_code=status.HTTP_201_CREATED)
async def create_habit_tracking(
    habit_data: HabitCreate,
    current_user: str = Depends(get_current_user)
):
    try:
        # Get AI analysis
        agent = HabitTrackerAgent(action="analyze", habit_data={"name": habit_data.habit_name})
        result = agent.run()
        
        return {
            "message": "Habit tracking created with AI insights",
            "insights": result
        }
    
    except Exception as e:
        logger.error(f"Error creating habit tracking: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing habit tracking"
        )

@app.post("/well-being-check-in/", status_code=status.HTTP_201_CREATED)
async def create_well_being_check_in(
    mood: int,
    energy: int,
    stress: int,
    notes: str,
    current_user: str = Depends(get_current_user)
):
    try:
        # Get AI analysis
        agent = CheckInAgent(metrics={"mood": mood, "energy": energy, "stress": stress, "notes": notes})
        result = agent.run()
        
        return {
            "message": "Well-being check-in created with AI insights",
            "insights": result
        }
    
    except Exception as e:
        logger.error(f"Error creating well-being check-in: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing well-being check-in"
        )

@app.get("/journal-entries/", response_model=list[JournalEntryResponse])
async def get_journal_entries(
    current_user: str = Depends(get_current_user),
    skip: int = 0,
    limit: int = 10
) -> list[JournalEntryResponse]:
    """Get all journal entries for the current user."""
    try:
        # In a real implementation, you would fetch from database
        # For now, returning mock data
        entries = [
            {
                "id": 1,
                "user_id": current_user,
                "entry_text": "Sample entry",
                "mood": "Positive",
                "created_at": datetime.utcnow(),
                "ai_insights": "Sample insights"
            }
        ]
        return [JournalEntryResponse(**entry) for entry in entries]
    except Exception as e:
        logger.error(f"Error fetching journal entries: {str(e)}")
        raise handle_database_error(e)

@app.get("/habits/", response_model=list[HabitResponse])
async def get_habits(
    current_user: str = Depends(get_current_user),
    skip: int = 0,
    limit: int = 10
) -> list[HabitResponse]:
    """Get all habits for the current user."""
    try:
        # Mock data for now
        habits = [
            {
                "id": 1,
                "user_id": current_user,
                "habit_name": "Daily Meditation",
                "frequency": "daily",
                "description": "15 minutes morning meditation",
                "streak": 5,
                "created_at": datetime.utcnow(),
                "last_logged": datetime.utcnow()
            }
        ]
        return [HabitResponse(**habit) for habit in habits]
    except Exception as e:
        logger.error(f"Error fetching habits: {str(e)}")
        raise handle_database_error(e)

@app.get("/check-ins/", response_model=list[CheckInResponse])
async def get_check_ins(
    current_user: str = Depends(get_current_user),
    skip: int = 0,
    limit: int = 10
) -> list[CheckInResponse]:
    """Get all check-ins for the current user."""
    try:
        # Mock data for now
        check_ins = [
            {
                "id": 1,
                "user_id": current_user,
                "mood": 8,
                "energy": 7,
                "stress": 3,
                "notes": "Feeling great today!",
                "created_at": datetime.utcnow()
            }
        ]
        return [CheckInResponse(**check_in) for check_in in check_ins]
    except Exception as e:
        logger.error(f"Error fetching check-ins: {str(e)}")
        raise handle_database_error(e)

# Error handlers
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    return handle_validation_error(exc)

@app.exception_handler(APIError)
async def api_error_handler(request, exc):
    return handle_api_error(exc)

async def generate_ai_reflection(text: str) -> dict:
    openai_client = AsyncOpenAI(api_key=settings.openai_api_key)
    
    response = await openai_client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "system",
                "content": """Analyze this journal entry as a mindfulness coach. Provide:
                1. A sentiment score between -1 (negative) and 1 (positive)
                2. Primary mood (one word)
                3. Three thought-provoking questions for deeper reflection
                4. Key themes identified
                Return JSON format only."""
            },
            {"role": "user", "content": text}
        ],
        response_format={"type": "json_object"}
    )
    
    return json.loads(response.choices[0].message.content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
