from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException, BackgroundTasks
from starlette.responses import JSONResponse
from datetime import datetime
from app.auth import get_current_user  # adjust as per your structure
from app.database import get_postgres_session
from app.api import commit_user_to_db
from app.models import User
from sqlmodel import Session

TIER_LIMITS = {
    "FREE": {"max_tokens": 50, "max_months": 3},
    "PRO": {"max_tokens": 500, "max_months": 12},
    "PREMIUM": {"max_tokens": 10000, "max_months": 36},
}

class RateLimiterMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method == "OPTIONS" or not str(request.url.path).startswith("/api"):
            return await call_next(request)
        session: Session = next(get_postgres_session())
        try:
            user = await get_current_user(request, session=session)
        except HTTPException:
            return JSONResponse({"detail": "Unauthorized"}, status_code=401)

        tier_info = TIER_LIMITS[user.tier.name]
        max_months = tier_info["max_months"]

        # Parse query parameters
        start_time = request.query_params.get("start_time")
        if start_time:
            try:
                start_timestamp = int(start_time) / 1e3
                start_date = datetime.fromtimestamp(start_timestamp)
                months_ago = (datetime.utcnow().year - start_date.year) * 12 + (datetime.utcnow().month - start_date.month)

                if months_ago > max_months:
                    return JSONResponse(
                        {"detail": f"{user.tier.name.title()} tier allows access to only last {max_months} months of data"},
                        status_code=403,
                    )
            except ValueError:
                return JSONResponse({"detail": "Invalid start_time"}, status_code=400)

        # Rate limiting logic based on token count
        if user.token_count <= 0:
            return JSONResponse(
                {"detail": "You have exhausted your usage quota. Upgrade your tier to continue."},
                status_code=429,
            )

        # Decrement token and commit
        user.token_count -= 1
        session.add(user)
        session.commit()
        return await call_next(request)
    