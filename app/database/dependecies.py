from typing import Annotated
from sqlmodel import Session
from fastapi import Depends
from app.database.postgres import postgresql_engine

def get_postgres_session():
    with Session(postgresql_engine) as session:
        yield session


PostgresSessionDep = Annotated[Session, Depends(get_postgres_session)]