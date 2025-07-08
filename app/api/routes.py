from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.responses import JSONResponse
from jose import jwt
from datetime import datetime, timedelta
from app.api.dependecies import (
    simple_moving_average,
    exponential_moving_average,
    relative_strength_index,
    moving_average_convergence_divergence,
    bollinger_band
)
router = APIRouter(prefix="/api", tags=["auth"])

@router.get("/")
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
