
from enum import Enum
from sqlmodel import Field, SQLModel
from typing import Optional
from app.database import postgresql_engine
from pydantic import PositiveInt, EmailStr
class TierEnum(Enum):
    FREE    = 0 # 50 tokens , SMA EMA , last 3 month of data
    PRO     = 1 # 500 token , access to SMA, EMA, RSI, MACD, last 1 year of data
    PREMIUM = 2 # unlimited , access to all data, all indicators, all 3 years of data

""" User Model

"""
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: EmailStr = Field(default=None, unique=True)
    password: str
    tier: TierEnum = Field(default=TierEnum.FREE, )
    token_count: PositiveInt= Field(default=50)

def create_db_and_tables():
    print("Creating and migrating database")
    SQLModel.metadata.create_all(postgresql_engine)