"""
Database Configuration and Session Management
SQLAlchemy setup for SQLite database
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from typing import Generator
from pathlib import Path

from models import Base

# ------------------------------------------------------------------
# DATABASE CONFIGURATION (Keep DB inside backend folder)
# ------------------------------------------------------------------

BASE_DIR = Path(__file__).parent.resolve()
DATABASE_PATH = BASE_DIR / "database.db"

DATABASE_URL = f"sqlite:///{DATABASE_PATH.as_posix()}"

# ------------------------------------------------------------------
# ENGINE
# ------------------------------------------------------------------

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False,
)

# ------------------------------------------------------------------
# SESSION
# ------------------------------------------------------------------

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ------------------------------------------------------------------
# INIT DB
# ------------------------------------------------------------------

def init_db():
    Base.metadata.create_all(bind=engine)
    print(f"✅ Database initialized at: {DATABASE_PATH}")

# ------------------------------------------------------------------
# DEPENDENCY
# ------------------------------------------------------------------

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------------------------------------------------------
# RESET (DEV ONLY)
# ------------------------------------------------------------------

def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print(f"⚠️ Database reset at: {DATABASE_PATH}")

# ------------------------------------------------------------------
# DIRECT RUN
# ------------------------------------------------------------------

if __name__ == "__main__":
    init_db()
    print(f"Database URL: {DATABASE_URL}")
    print(f"Database Path: {DATABASE_PATH}")
