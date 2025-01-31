# Mind Mirror

An AI-powered journaling and self-reflection app that helps users track their personal growth journey.

## Features

- Journal entries with AI-powered insights
- Mood tracking and analysis
- Habit tracking
- Personal growth insights

## Tech Stack

- Backend: FastAPI + PostgreSQL
- ORM: SQLAlchemy
- Migrations: Alembic
- AI Integration: OpenAI API

## Project Structure

```
mind_mirror/
├── app/                    # Application code
│   ├── api/               # API endpoints
│   ├── core/              # Core functionality
│   ├── models/            # Database models
│   └── schemas/           # Pydantic models
├── migrations/            # Database migrations
├── alembic.ini           # Alembic configuration
├── main.py               # Application entry point
└── requirements.txt      # Project dependencies
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables in `.env`:
```
DATABASE_URL=postgresql://user:pass@localhost/mindmirror
OPENAI_API_KEY=your-api-key
```

4. Run database migrations:
```bash
alembic upgrade head
```

5. Start the server:
```bash
uvicorn main:app --reload
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
