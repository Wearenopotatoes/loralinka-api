from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request, Response
import os
import logging

logger = logging.getLogger(__name__)

def get_rate_limit_key(request: Request):
    client_ip = get_remote_address(request)
    api_key = request.headers.get("X-API-Key")

    # Always rate limit by combination of API key + IP
    # This allows multiple users per API key but prevents single IP abuse
    return f"api_key:{api_key}:ip:{client_ip}"

def create_limiter():
    redis_url = os.getenv("REDIS_URL")
    storage_uri = "memory://"

    if redis_url:
        try:
            # Test if Redis is available
            import redis
            client = redis.from_url(redis_url)
            client.ping()
            storage_uri = redis_url
            logger.info("Using Redis for rate limiting")
        except Exception as e:
            logger.warning(f"Redis not available, falling back to memory storage: {e}")

    return Limiter(
        key_func=get_rate_limit_key,
        default_limits=["500/minute", "5000/hour"],  # Higher limits since it's per API key + IP combo
        storage_uri=storage_uri
    )

limiter = create_limiter()

def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    response = Response(
        content=f"Rate limit exceeded: {exc.detail}",
        status_code=429,
        headers={"Content-Type": "text/plain"}
    )
    response = request.app.state.limiter._inject_headers(response, request.state.view_rate_limit)
    return response