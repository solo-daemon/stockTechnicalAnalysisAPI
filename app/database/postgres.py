from sqlmodel import create_engine
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

PG_DB_NAME=os.getenv("PG_DB_NAME")
PG_DB_USER=os.getenv("PG_DB_USER")
PG_DB_PASSWORD=os.getenv("PG_DB_PASSWORD")
PG_DB_HOST=os.getenv("PG_DB_HOST")
PG_DB_PORT=os.getenv("PG_DB_PORT")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql+psycopg2://{PG_DB_USER}:{PG_DB_PASSWORD}@{PG_DB_HOST}:{PG_DB_PORT}/{PG_DB_NAME}"
)
# Thread pool by default; SQLAlchemy manages it
postgresql_engine = create_engine(
    DATABASE_URL,
    echo=True,  # optional: logs SQL queries
    pool_size=10,           # number of threads in pool
    max_overflow=20,        # how many more it can grow
    pool_pre_ping=True,     # checks connections are alive
)

async def get_user_info_from_db(user_id: str) -> dict:
    # Fetch from users table
    return {"user_id": user_id, "tier": "pro"}

async def update_user_rate_data_in_db(user_id: str, minute_window: int, count: int):
    # Store in audit logs or analytics
    pass

