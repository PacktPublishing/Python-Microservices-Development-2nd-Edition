from contextlib import asynccontextmanager

from quart import Quart
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy import update

#
# SA Engine init
#
DATABASE_URL = "sqlite+aiosqlite:///./test.db"
engine = create_async_engine(DATABASE_URL, future=True, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()


#
# Data Model
#
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    author = Column(String, nullable=False)
    release_year = Column(Integer, nullable=False)

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "author": self.author,
            "release_year": self.release_year,
        }


#
# Data Access Layer
#
class BookDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create_book(self, name: str, author: str, release_year: int):
        new_book = Book(name=name, author=author, release_year=release_year)
        self.db_session.add(new_book)
        await self.db_session.flush()
        return new_book.json()

    async def get_all_books(self) -> List[Book]:
        q = await self.db_session.execute(select(Book).order_by(Book.id))
        return {"books": [b.json() for b in q.scalars().all()]}

    async def get_book(self, book_id) -> Book:
        q = select(Book).where(Book.id == book_id)
        q = await self.db_session.execute(q)
        b = q.one()
        return b[0].json()

    async def update_book(
        self,
        book_id: int,
        name: Optional[str],
        author: Optional[str],
        release_year: Optional[int],
    ):
        q = update(Book).where(Book.id == book_id)
        if name:
            q = q.values(name=name)
        if author:
            q = q.values(author=author)
        if release_year:
            q = q.values(release_year=release_year)
        q.execution_option
        await self.db_session.execute(q)
        return get_book(book_id)


#
# Quart App
#
app = Quart(__name__)


@app.before_serving
async def startup():
    # create db tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        async with book_dal() as bd:
            await bd.create_book("name", "author", 2010)


@asynccontextmanager
async def book_dal():
    async with async_session() as session:
        async with session.begin():
            yield BookDAL(session)


@app.post("/books")
async def create_book(name: str, author: str, release_year: int):
    async with book_dal() as bd:
        await bd.create_book(name, author, release_year)


@app.get("/books/<int:book_id>")
async def get_book(book_id: int):
    async with book_dal() as bd:
        return await bd.get_book(book_id)


@app.get("/books")
async def get_all_books() -> List[Book]:
    async with book_dal() as bd:
        return await bd.get_all_books()


@app.put("/books/<int:book_id>")
async def update_book(
    book_id: int,
    name: Optional[str] = None,
    author: Optional[str] = None,
    release_year: Optional[int] = None,
):
    async with book_dal() as bd:
        return await bd.update_book(book_id, name, author, release_year)


if __name__ == "__main__":
    app.run(port=1111, host="127.0.0.1")
