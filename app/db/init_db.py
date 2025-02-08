from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import Base

load_dotenv()

DATABASE_URL = "postgresql://jamesguy@localhost/mindmirror"
engine = create_engine(DATABASE_URL)

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Database tables created successfully!")
