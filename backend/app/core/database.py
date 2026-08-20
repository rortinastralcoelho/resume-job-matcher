from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

# Create the database engine
engine = create_engine(settings.DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# This Base class is what all our models will inherit from
Base = declarative_base()

def get_db():
    """Dependency to get the database session for our API routes."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()