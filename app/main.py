from typing import Union
from fastapi import FastAPI
from app.crud import (
    simple_moving_average,
    exponential_moving_average,
    relative_strength_index,
    moving_average_convergence_divergence,
    bollinger_band,
)

app = FastAPI()

@app.get('/api')
async def calculate_data(company_symbol: str | None = None, start_time: int | None = None, end_time: int | None = None):
    result = {
        "SMA":  simple_moving_average(company_symbol=company_symbol, start_time=start_time, end_time=end_time),    # simple moving average   
        "EMA":  exponential_moving_average(company_symbol=company_symbol, start_time=start_time, end_time=end_time),    # exponential Moving Average   
        "RSI":  relative_strength_index(company_symbol=company_symbol, start_time=start_time, end_time=end_time),    # relative Strength Index   
        "MACD": moving_average_convergence_divergence(company_symbol=company_symbol, start_time=start_time, end_time=end_time),    # moving Average Convergence Divergence
        "BB":   bollinger_band(company_symbol=company_symbol, start_time=start_time, end_time=end_time),    # bollinger Bands
    }
    return result
