from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Engine - actual connection to the database
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False}  # Only needed for SQLite
)

# Session - used to talk to the DB in each request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base - all our models will inherit from this
Base = declarative_base()

# Dependency - gives each request its own DB session, closes it after
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()