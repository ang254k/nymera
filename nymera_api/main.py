from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.routers import auth_router, sueno_router, comentario_router, home_router, categoria_router, notificacion_router, usuario_router, busqueda_router, hashtag_router

from app.repositories.security_log_repository import SecurityLogRepository

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware

from app.limiter import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.config import settings

app = FastAPI(title="Nymera API")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

security_log_repo = SecurityLogRepository()

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )

# ==========================
# Security Headers Middleware
# ==========================
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Frame-Options"] = "DENY"    # Evita ataques de Clickjacking (iframes)
        response.headers["X-Content-Type-Options"] = "nosniff"  # Bloquea la suplantación de tipos MIME
        response.headers["X-XSS-Protection"] = "1; mode=block"  # Protección extra contra XSS básico
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin" # Controla la privacidad de la URL de origen
        return response

app.add_middleware(SecurityHeadersMiddleware)

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    client_ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")
    
    security_log_repo.create_log(
        evento="RATE_LIMIT_EXCEEDED",
        ip_address=client_ip,
        user_agent=user_agent,
        exito=False
    )
    
    return JSONResponse(
        status_code=429,
        content={"detail": "wait_a_moment"}
    )

@app.exception_handler(PermissionError)
async def permission_error_handler(request: Request, exc: PermissionError):
    return JSONResponse(
        status_code=403,
        content={"detail": str(exc)}
    )
    
app.include_router(auth_router.router)
app.include_router(sueno_router.router)
app.include_router(comentario_router.router)
app.include_router(home_router.router)
app.include_router(categoria_router.router)
app.include_router(notificacion_router.router)
app.include_router(usuario_router.router)
app.include_router(busqueda_router.router)
app.include_router(hashtag_router.router)
