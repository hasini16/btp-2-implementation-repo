import os
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

# Supabase PostgreSQL connection string
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres.clgjswrlcwzmdxhhegtk:adhithya365@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"
)

# Use asyncpg for async support (install asyncpg if needed, but psycopg2-binary works with sync for simplicity)
# For full async: pip install asyncpg; DATABASE_URL = DATABASE_URL.replace('postgresql://', 'postgresql+asyncpg://')
engine = create_engine(DATABASE_URL, echo=False)

AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def get_db():
    """Dependency to get DB session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
