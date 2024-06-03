""""Middleware for authorization."""
import time

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware


class AuthorizationMiddleware(BaseHTTPMiddleware):
    """Middleware for authorization."""

    def __init__(self, app: FastAPI) -> None:
        """Initialize the middleware."""
        super().__init__(app)
        # self.auth = auth  # noqa: ERA001

    async def dispatch(self, request: Request, call_next) -> None:  # noqa: ANN001
        """Dispatch the request."""
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        # print(f'Process time: {process_time}')  # noqa: ERA001
        response.headers['X-Process-Time'] = str(process_time)
        return response
