# Section 1: Database connection and session management
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Section 2: Create SQLAlchemy engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# Section 3: Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Section 4: Create base class for models
Base = declarative_base()

# Section 5: Dependency to get database session
def get_db():
    """Get database session dependency for FastAPI"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()