from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.routers import auth_router, sueno_router, comentario_router, home_router, categoria_router, notificacion_router, usuario_router, busqueda_router, hashtag_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import settings

app = FastAPI(title="Nymera API")

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
