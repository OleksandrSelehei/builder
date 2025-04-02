from datetime import datetime
from sqlalchemy import Integer, func
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from Utils.Config.config import settings

DATABASE_URL = settings.get_db_url()

# Create an asynchronous engine for database interaction
engine = create_async_engine(url=DATABASE_URL)

# Create an async session factory for database transactions
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

# Base class for all models
class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True  # Abstract class to prevent table creation for it

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """Automatically generate table name based on class name."""
        return cls.__name__.lower() + 's'
