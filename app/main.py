from typing import Union
from fastapi import FastAPI

from sqlmodel import SQLModel
from app.database import postgresql_engine
from app.api import api_router
from app.middleware import (
    RateLimiterMiddleware,
    DBSessionMiddleware
    )
import uvicorn


from app.models import create_db_and_tables

from app.auth import (
    auth_router,
)

app = FastAPI()


app.add_event_handler("startup", create_db_and_tables)

# app.add_middleware(DBSessionMiddleware)
app.add_middleware(RateLimiterMiddleware)
app.include_router(auth_router)
app.include_router(api_router)

