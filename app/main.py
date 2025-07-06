from typing import Union
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from sqlmodel import SQLModel
from app.database import postgresql_engine
from app.api import (
    simple_moving_average,
    exponential_moving_average,
    relative_strength_index,
    moving_average_convergence_divergence,
    bollinger_band,
)
from app.middleware import (
    CacheMiddleware,
    RateLimiterMiddleware
)

from app.models import create_db_and_tables

from app.auth import (
    auth_router,
    get_current_user
)

def on_startup():
    
    SQLModel.metadata.create_all(postgresql_engine)

app = FastAPI()


app.add_event_handler("startup", create_db_and_tables)

# app.add_middleware(CacheMiddleware)
# app.add_middleware(RateLimiterMiddleware)
app.include_router(auth_router)

@app.get('/api')
async def calculate_data(company_symbol: str | None = None, start_time: int | None = None, end_time: int | None = None):
    print(company_symbol)
    result = {
        "SMA":  await simple_moving_average(company_symbol=company_symbol, start_time=start_time, end_time=end_time),    # simple moving average   
        "EMA":  await exponential_moving_average(company_symbol=company_symbol, start_time=start_time, end_time=end_time),    # exponential Moving Average   
        "RSI":  await relative_strength_index(company_symbol=company_symbol, start_time=start_time, end_time=end_time),    # relative Strength Index   
        "MACD": await moving_average_convergence_divergence(company_symbol=company_symbol, start_time=start_time, end_time=end_time),    # moving Average Convergence Divergence
        "BB":   await bollinger_band(company_symbol=company_symbol, start_time=start_time, end_time=end_time),    # bollinger Bands
    }
    return JSONResponse(content=result, status_code=status.HTTP_200_OK)
