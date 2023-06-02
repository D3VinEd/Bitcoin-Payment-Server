from slowapi import _rate_limiter, RateLimitMiddleware
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from starlette.requests import Request
from fastapi import HTTPException
from slowapi.

async def _check_rate_limit(request: Request):
    try:
        limiter.check_rate_limit(str(request.url.path), get_remote_address(request))
    except RateLimitExceeded:
        raise HTTPException(
            status_code=429, detail="Too many requests"
        )