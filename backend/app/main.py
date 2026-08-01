import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.routers.review import router

configure_logging()
settings = get_settings()
limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="CodeMedic AI", version="1.0.0", description="Agentic GitHub repository reviewer")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(CORSMiddleware, allow_origins=settings.origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(router)

@app.get("/")
def root():
    return {"name": "CodeMedic AI API", "status": "ok", "docs": "/docs", "health": "/health"}

@app.get("/health")
@limiter.limit("60/minute")
def health(request: Request): return {"status": "ok"}

@app.exception_handler(Exception)
async def unhandled_exception(_: Request, exc: Exception):
    logging.getLogger(__name__).exception("Unhandled API error")
    return JSONResponse(status_code=500, content={"detail": "An unexpected error occurred."})

settings = get_settings()
print("Origins:", settings.origins)