"""
Database Configuration and Session Management
SQLAlchemy setup for SQLite database
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from typing import Generator
import os
from pathlib import Path

from models import Base

# Database configuration
DATABASE_DIR = Path(__file__).parent.parent / "data"
DATABASE_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_PATH = DATABASE_DIR / "database.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite specific
    poolclass=StaticPool,  # Better for SQLite
    echo=False  # Set True for SQL query logging
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize database - create all tables"""
    Base.metadata.create_all(bind=engine)
    print(f"✅ Database initialized at: {DATABASE_PATH}")


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency for database sessions
    Usage:
        @app.get("/")
        def endpoint(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def reset_db():
    """Drop all tables and recreate (DANGEROUS - use only in development)"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print(f"⚠️  Database reset at: {DATABASE_PATH}")


# Initialize database on import (optional - can be called explicitly)
if not DATABASE_PATH.exists():
    init_db()


if __name__ == "__main__":
    # Test database connection
    init_db()
    print(f"Database URL: {DATABASE_URL}")
    print(f"Database Path: {DATABASE_PATH}")
    print(f"Tables created: {Base.metadata.tables.keys()}")