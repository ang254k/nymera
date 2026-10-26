from fastapi import APIRouter, HTTPException, Depends, Request

from app.schemas.auth_schema import (
    ForgotPasswordRequest,
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    ResetPasswordRequest
)
from app.schemas.usuario_schema import UsuarioResponse

from app.services.auth_service import AuthService
from app.services.usuario_service import UsuarioService
from app.repositories.usuario_repository import UsuarioRepository

from app.utils.jwt_handler import create_access_token
from app.dependencies.auth import get_current_user
from app.models.usuario import Usuario

from app.limiter import limiter

router = APIRouter(prefix="/auth", tags=["auth"])

usuario_service = UsuarioService(UsuarioRepository())
auth_service = AuthService()


@router.post("/register", response_model=UsuarioResponse)
@limiter.limit("4/minute")
def register(request: Request, data: RegisterRequest):

    try:
        usuario = usuario_service.register(data.nombre, data.email, data.password)

        if usuario is None:
            raise HTTPException(status_code=400, detail="email_already_registered")

        return usuario

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=TokenResponse)
@limiter.limit("5/minute")
def login(request: Request, data: LoginRequest):
    usuario = usuario_service.login(data.email, data.password)

    if usuario is None:
        raise HTTPException(status_code=401, detail="invalid_credentials")
    token = create_access_token({"sub": str(usuario.id)})

    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UsuarioResponse)
def me(current_user: Usuario = Depends(get_current_user)):
    return current_user


@router.post("/forgot-password")
@limiter.limit("4/minute")
def forgot_password(request: Request, data: ForgotPasswordRequest):
    return auth_service.forgot_password(data.email)


@router.post("/reset-password")
@limiter.limit("3/minute")
def reset_password(request: Request, data: ResetPasswordRequest):
    try:
        return auth_service.reset_password(data.token, data.new_password)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
