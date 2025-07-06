
from enum import Enum
from sqlmodel import Field, SQLModel
from typing import Optional
from app.database import postgresql_engine
class TierEnum(Enum):
    FREE    = 0 # 50 tokens , SMA EMA , last 3 month of data
    PRO     = 1 # 500 token , access to SMA, EMA, RSI, MACD, last 1 year of data
    PREMIUM = 2 # unlimited , access to all data, all indicators, all 3 years of data

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str
    password: str
    tier: TierEnum = Field(default=0, )
    token_count: int= Field(default=50)
    jwt_access_token: Optional[int] = Field(default=None, index=True, unique=True)
    jwt_refresh_token: Optional[int] = Field(default=None, index=True, unique=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(postgresql_engine)