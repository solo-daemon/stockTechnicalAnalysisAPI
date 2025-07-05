import polars as pl
from datetime import datetime
from pydantic import BaseModel

class QueryStructure(BaseModel):
    company_symbol: str = None
    start_time: datetime = None
    end_time:   datetime = None

m = QueryStructure(
    comapny_symbol = "BSE",
    start_time=1656633600000,
    end_time=1656892800000,
)

df = pl.read_parquet("../../stocks_ohlc_data.parquet")

async def simple_moving_average(company_symbol: str | None, start_time: int | None, end_time: int | None):
    # if company_symbol == None or start_time == None or end_time == None:

    pass

async def exponential_moving_average(company_symbol: str | None, start_time: int | None, end_time: int | None):
    # if company_symbol == None or start_time == None or end_time == None:

    pass

async def relative_strength_index(company_symbol: str | None, start_time: int | None, end_time: int | None):
    # if company_symbol == None or start_time == None or end_time == None:

    pass

async def moving_average_convergence_divergence(company_symbol: str | None, start_time: int | None, end_time: int | None):
    # if company_symbol == None or start_time == None or end_time == None:

    pass

async def moving_average_convergence_divergence(company_symbol: str | None, start_time: int | None, end_time: int | None):
    # if company_symbol == None or start_time == None or end_time == None:

    pass

async def bollinger_band(company_symbol: str | None, start_time: int | None, end_time: int | None):
    pass