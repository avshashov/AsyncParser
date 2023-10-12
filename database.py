import os

from dotenv import load_dotenv
from sqlalchemy import ARRAY, String
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

import schema

load_dotenv()

DSN = (f'postgresql+asyncpg://'
       f'{os.getenv("USER")}:'
       f'{os.getenv("PASSWORD")}@'
       f'{os.getenv("HOST")}:'
       f'{os.getenv("PORT")}/'
       f'{os.getenv("DATABASE")}')

engine = create_async_engine(DSN, echo=True)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class Character(Base):
    __tablename__ = 'character'

    id: Mapped[int] = mapped_column(primary_key=True)
    birth_year: Mapped[str]
    eye_color: Mapped[str]
    films: Mapped[list[str]] = mapped_column(ARRAY(String))
    gender: Mapped[str]
    hair_color: Mapped[str]
    height: Mapped[str]
    homeworld: Mapped[str]
    mass: Mapped[str]
    name: Mapped[str]
    skin_color: Mapped[str]
    species: Mapped[list[str] | list] = mapped_column(ARRAY(String), nullable=True)
    starships: Mapped[list[str] | list] = mapped_column(ARRAY(String), nullable=True)
    vehicles: Mapped[list[str] | list] = mapped_column(ARRAY(String), nullable=True)


async def create_table() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def create_character(character: schema.Character) -> None:
    async with async_session() as session_db:
        data = Character(**character.model_dump())
        session_db.add(data)
        await session_db.commit()
