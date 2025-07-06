from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi import status
from app.cache import get_redis_cache
from app.auth.dependencies import get_current_user  # adjust path as needed
import time

# API call limits per minute based on tier
TIER_LIMITS = {
    "free": 10,
    "pro": 100,
    "premium": 1000
}

class RateLimiterMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method == "OPTIONS":
            return await call_next(request)

        try:
            user = await get_current_user(request)
        except Exception:
            return JSONResponse({"detail": "Unauthorized"}, status_code=401)

        user_id = user["user_id"]
        tier = user.get("tier", "free")
        max_requests = TIER_LIMITS.get(tier, 10)

        redis_cache = get_redis_cache()
        client = await redis_cache.get_client()

        # Redis key for this user's request count
        current_window = int(time.time() // 60)
        redis_key = f"rate:{user_id}:{current_window}"

        current = await client.get(redis_key)
        current = int(current) if current else 0

        if current >= max_requests:
            return JSONResponse(
                {"detail": f"Rate limit exceeded for {tier} user"},
                status_code=status.HTTP_429_TOO_MANY_REQUESTS
            )

        # Increment counter and set expiry
        pipe = client.pipeline()
        pipe.incr(redis_key)
        pipe.expire(redis_key, 60)  # expire after 1 min
        await pipe.execute()

        return await call_next(request)