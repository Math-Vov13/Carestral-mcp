"""Database configuration and session management."""

import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Parse and clean the URL for asyncpg compatibility
parsed = urlparse(DATABASE_URL)
query_params = parse_qs(parsed.query)

# Remove sslmode and channel_binding from query params (not compatible with asyncpg)
query_params.pop('sslmode', None)
query_params.pop('channel_binding', None)

# Flatten query params (parse_qs returns lists)
clean_query = urlencode({k: v[0] for k, v in query_params.items()})

# Reconstruct URL
clean_url = urlunparse((
    parsed.scheme,
    parsed.netloc,
    parsed.path,
    parsed.params,
    clean_query,
    parsed.fragment
))

# Convert postgresql:// to postgresql+asyncpg:// if needed
if clean_url.startswith("postgresql://"):
    DATABASE_URL = clean_url.replace("postgresql://", "postgresql+asyncpg://", 1)
elif not clean_url.startswith("postgresql+asyncpg://"):
    DATABASE_URL = f"postgresql+asyncpg://{clean_url}"
else:
    DATABASE_URL = clean_url

# Create async engine with SSL enabled
engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL query logging
    pool_pre_ping=True,  # Verify connections before using them
    pool_size=10,
    max_overflow=20,
    connect_args={
        "ssl": "require",  # Enable SSL for NeonDB
    }
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Create declarative base for models
Base = declarative_base()


@asynccontextmanager
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """Initialize database tables and extensions."""
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS fuzzystrmatch"))
        await conn.run_sync(Base.metadata.create_all)
