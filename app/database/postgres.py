from sqlmodel import create_engine
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+psycopg2://myuser:mypassword@localhost:5433/mydatabase"
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

