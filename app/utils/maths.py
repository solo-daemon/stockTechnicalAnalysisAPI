import polars as pl

df = pl.read_parquet("../../stocks_ohlc_data.parquet")

# print(df.head(4))