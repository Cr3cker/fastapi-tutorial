# In this file, I am going to show you how to work with SQLAlchemy ORM
# Here we are going to use SQLite as DBMS

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


# Connection string
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# If you are using PostgreSQL
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

# Creating the engine ("check_same_thread" argument is used only for SQLite)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

Base = declarative_base()


class Person(Base):
    __tablename__ = "people"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)


# Create tables
Base.metadata.create_all(bind=engine)

# This app does nothing
app = FastAPI()

# After you run this file, sql_app.db file will be automatically generated.
# You can open it using DB Browser for SQLite
