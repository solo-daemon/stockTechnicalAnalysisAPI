from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from app.cache import get_redis_cache

class CacheMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method != "GET":
            return await call_next(request)

        redis_cache = get_redis_cache()
        client = await redis_cache.get_client()

        cache_key = f"cache:{request.url.path}?{request.url.query}"
        cached_data = await client.get(cache_key)
        
        if cached_data:
            return JSONResponse(content=eval(cached_data))  # or use json.loads if serialized

        response = await call_next(request)

        if response.status_code == 200:
            body = b""
            async for chunk in response.body_iterator:
                body += chunk
            await client.set(cache_key, body.decode(), ex=60)  # cache for 60 seconds
            return JSONResponse(content=eval(body.decode()))  # return original response

        return response