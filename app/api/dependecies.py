import polars as pl
from datetime import datetime, date, time
from pydantic import BaseModel, FilePath, field_validator, ValidationError
from pathlib import Path
from functools import lru_cache
from typing import Optional
from app.models import User
from app.database import get_postgres_session
from sqlmodel import Session
class QueryStructure(BaseModel):
    symbol: str
    start_time: datetime
    end_time:   datetime

    @field_validator("start_time", "end_time", mode="before")
    @classmethod
    def parse_nanosecond_timestamp(cls, v):
        if isinstance(v, int):
            # Convert nanoseconds -> microseconds, then create datetime (naive)
            return datetime.fromtimestamp(v / 1e3)
        return v

m = QueryStructure(
    symbol = 'TATASTEEL',
    start_time=1656633600000,
    end_time=1656979200000,
)

async def commit_user_to_db(user: User):
    session: Session = next(get_postgres_session())
    print("hello")
    session.add(user)
    print("world")
    session.commit()
    session.close()
    return

@lru_cache
def read_file():
    validated_path: FilePath = FilePath(
    Path(__file__).resolve().parent.parent / "data" / "stocks_ohlc_data.parquet"
    )
    df = pl.read_parquet(str(validated_path))
    return df

def filter_data(df: pl.DataFrame, company_symbol: str, start_time: int, end_time: int) -> pl.DataFrame | ValidationError:
    type(company_symbol)
    try:
        query = QueryStructure(
        symbol=company_symbol,
        start_time=start_time,
        end_time=end_time,
        )
    except ValidationError:
        return ValidationError
    return df.filter(
        (pl.col("symbol") == query.symbol)  &
        (pl.col("date") >= query.start_time) &
        (pl.col("date") <= query.end_time)
    )


async def simple_moving_average(company_symbol: str, start_time: int, end_time: int, window: int = 14):
    if not all([company_symbol, start_time, end_time]):
        return 0

    df = read_file()
    filtered = filter_data(df, company_symbol, start_time, end_time)
    result = filtered.with_columns([
        pl.col("date").dt.strftime("%Y-%m-%d %H:%M:%S").alias("date"),  # make datetime serializable
        pl.col("close").rolling_mean(window_size=window).alias(f"SMA_{window}")
    ])
    return result.to_dicts()


async def exponential_moving_average(company_symbol: Optional[str], start_time: Optional[int], end_time: Optional[int], window: int = 14):
    if not all([company_symbol, start_time, end_time]):
        return 0

    df = read_file()
    filtered = filter_data(df, company_symbol, start_time, end_time)

    result = filtered.with_columns([
        pl.col("date").dt.strftime("%Y-%m-%d %H:%M:%S").alias("date"),  # make datetime serializable
        pl.col("close").rolling_mean(window_size=window).alias(f"EMA_{window}")
    ])
    return result.to_dicts()


async def relative_strength_index(company_symbol: Optional[str], start_time: Optional[int], end_time: Optional[int], period: int = 14):
    if not all([company_symbol, start_time, end_time]):
        return 0

    df = read_file()
    filtered = filter_data(df, company_symbol, start_time, end_time)

    delta = filtered.select([
        pl.col("close").diff().alias("delta")
    ])

    gains = delta.with_columns([
        pl.when(pl.col("delta") > 0).then(pl.col("delta")).otherwise(0).alias("gain"),
        pl.when(pl.col("delta") < 0).then(-pl.col("delta")).otherwise(0).alias("loss")
    ])

    avg_gain = gains["gain"].ewm_mean(span=period)
    avg_loss = gains["loss"].ewm_mean(span=period)

    rs = avg_gain / (avg_loss + 1e-10)  # prevent div-by-zero
    rsi = 100 - (100 / (1 + rs))

    result = filtered.with_columns([
         pl.col("date").dt.strftime("%Y-%m-%d %H:%M:%S").alias("date"),  # make datetime serializable
        rsi.alias(f"RSI_{period}")
    ])
    return result.to_dicts()


async def moving_average_convergence_divergence(company_symbol: Optional[str], start_time: Optional[int], end_time: Optional[int], fast: int = 12, slow: int = 26, signal: int = 9):
    if not all([company_symbol, start_time, end_time]):
        return 0

    df = read_file()
    filtered = filter_data(df, company_symbol, start_time, end_time)

    ema_fast = pl.col("close").ewm_mean(span=fast).alias("ema_fast")
    ema_slow = pl.col("close").ewm_mean(span=slow).alias("ema_slow")

    macd_line = (ema_fast - ema_slow).alias("macd_line")
    signal_line = macd_line.ewm_mean(span=signal).alias("signal_line")
    histogram = (macd_line - signal_line).alias("macd_hist")

    result = filtered.with_columns([
        pl.col("date").dt.strftime("%Y-%m-%d %H:%M:%S").alias("date"),  # make datetime serializable
        ema_fast,
        ema_slow,
        macd_line,
        signal_line,
        histogram
    ])
    return result.to_dicts()


async def bollinger_band(company_symbol: Optional[str], start_time: Optional[int], end_time: Optional[int], period: int = 20, stddev_multiplier: float = 2.0):
    if not all([company_symbol, start_time, end_time]):
        return 0

    df = read_file()
    filtered = filter_data(df, company_symbol, start_time, end_time)

    sma = pl.col("close").rolling_mean(window_size=period).alias("BB_MID")
    rolling_std = pl.col("close").rolling_std(window_size=period).alias("BB_STD")

    upper_band = (sma + stddev_multiplier * rolling_std).alias("BB_UPPER")
    lower_band = (sma - stddev_multiplier * rolling_std).alias("BB_LOWER")

    result = filtered.with_columns([
        pl.col("date").dt.strftime("%Y-%m-%d %H:%M:%S").alias("date"),  # make datetime serializable
        sma,
        upper_band,
        lower_band
    ])
    return result.to_dicts()
