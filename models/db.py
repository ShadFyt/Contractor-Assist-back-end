from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from config import settings


SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    """opens & closes a connection(session) to the database

    Yields:
        session: establishes and maintains all conversations between your program and the databases
    """
    with Session(engine) as session:
        yield session


# TODO implement async version
# async def get_async_session() -> AsyncSession:
#     # add aiosqlite
#     async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

#     async with async_session() as session:
#         yield session
