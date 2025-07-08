from app.database.postgres import (
    get_user_info_from_db,
    update_user_rate_data_in_db,
    postgresql_engine
)

from app.database.dependecies import(
    PostgresSessionDep,
    get_postgres_session
)