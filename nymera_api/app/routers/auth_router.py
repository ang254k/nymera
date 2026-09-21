from fastapi import APIRouter, HTTPException, Depends

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

router = APIRouter(prefix="/auth", tags=["auth"])

usuario_service = UsuarioService(UsuarioRepository())
auth_service = AuthService()


@router.post("/register", response_model=UsuarioResponse)
def register(data: RegisterRequest):

    try:
        usuario = usuario_service.register(data.nombre, data.email, data.password)

        if usuario is None:
            raise HTTPException(status_code=400, detail="Email ya registrado")

        return usuario

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest):

    usuario = usuario_service.login(data.email, data.password)

    if usuario is None:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    token = create_access_token({"sub": str(usuario.id)})

    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UsuarioResponse)
def me(current_user: Usuario = Depends(get_current_user)):
    return current_user


@router.post("/forgot-password")
def forgot_password(data: ForgotPasswordRequest):
    return auth_service.forgot_password(data.email)


@router.post("/reset-password")
def reset_password(data: ResetPasswordRequest):
    try:
        return auth_service.reset_password(data.token, data.new_password)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
