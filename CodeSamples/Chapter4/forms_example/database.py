# sqlachemy-async.py
from contextlib import asynccontextmanager

from quart import Quart
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, Boolean, JSON
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy import update
from werkzeug.security import generate_password_hash, check_password_hash

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
    password = Column(String)
    config = Column(JSON)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def json(self):
        return {
            "id": self.id,
            "email": self.email,
            "slack_id": self.slack_id,
            "config": self.config,
            "is_active": self.is_active,
            "is_admin": self.is_admin,
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
        password=None,
        config=None,
        is_active=True,
        is_admin=False,
    ):
        new_user = User(
            name=name,
            email=email,
            slack_id=slack_id,
            password=password,
            config=config,
            is_active=is_active,
            is_admin=is_admin,
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user.json()

    async def get_all_users(self):
        query_result = await self.db_session.execute(select(User).order_by(User.id))
        return [user.json() for user in query_result.scalars().all()]

    async def get_user(self, user_id):
        query = select(User).where(User.id == user_id)
        query_result = await self.db_session.execute(query)
        user = query_result.one()
        return user[0].json()

    async def set_password(self, user_id, password):
        query = select(User).where(User.id == user_id)
        query_result = await self.db_session.execute(query)
        user = query_result.one()[0]
        user.set_password(password)
        await self.db_session.flush()

    async def authenticate(self, user_id, password):
        query = select(User).where(User.id == user_id)
        query_result = await self.db_session.execute(query)
        user = query_result.one()[0]
        return user.check_password(password)


async def initialize_database():
    # create db tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        async with user_dal() as bd:
            await bd.create_user("name", "email", "slack_id")


@asynccontextmanager
async def user_dal():
    async with async_session() as session:
        async with session.begin():
            yield UserDAL(session)
