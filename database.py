from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

engine = create_engine(settings.DATABASE_URL, future=True, pool_pre_ping=True)

# Each request gets its own isolated session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True,
)

Base = declarative_base()


def get_db():
    """
    Provides a database session per request.
    yield ensures session always closes after request completes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        