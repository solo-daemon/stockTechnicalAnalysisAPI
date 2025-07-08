from starlette.middleware.base import BaseHTTPMiddleware
from sqlmodel import Session
from app.database import postgresql_engine

class DBSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        with Session(postgresql_engine) as session:
            request.state.session = session
            response = await call_next(request)
            session.close()
            return response