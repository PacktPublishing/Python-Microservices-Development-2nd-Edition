# sqlachemy-async.py
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, Boolean, JSON
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy import update

# Initialize SQLAlchemy with a test database
DATABASE_URL = "sqlite+aiosqlite:///./test.db"
engine = create_async_engine(DATABASE_URL, future=True, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()


# Data Model
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String)
    slack_id = Column(String)
    location = Column(String)

    def json(self):
        return {
            "id": self.id,
            "email": self.email,
            "slack_id": self.slack_id,
            "location": self.location,
        }


# Data Access Layer
class UserDAL:
    def __init__(self, db_session):
        self.db_session = db_session

    async def create_user(
        self,
        name,
        email,
        slack_id,
        location,
    ):
        new_user = User(
            name=name,
            email=email,
            slack_id=slack_id,
            location=location,
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user.json()

    async def get_all_users(self):
        query_result = await self.db_session.execute(select(User).order_by(User.id))
        return {"users": [user.json() for user in query_result.scalars().all()]}

    async def get_user(self, user_id):
        query = select(User).where(User.id == user_id)
        query_result = await self.db_session.execute(query)
        user = query_result.one()
        return user[0].json()

    async def get_users_with_locations(self):
        query = select(User).where(User.location is not None)
        return await self.db_session.execute(query)


@asynccontextmanager
async def user_dal():
    async with async_session() as session:
        async with session.begin():
            yield UserDAL(session)


async def database_startup():
    # create db tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        async with user_dal() as bd:
            await bd.create_user("alice", "email", "slack_id", "London, UK")
            await bd.create_user("bob", "email", "slack_id", "Paris, France")
