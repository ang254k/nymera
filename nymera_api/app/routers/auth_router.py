import os
import requests

from app.config import settings

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
    #Validar token con Turnstile
    turnstile_secret = settings.TURNSTILE_SECRET_KEY
    
    if turnstile_secret:
        verify_url = "https://challenges.cloudflare.com/turnstile/v0/siteverify"
        
        payload = {
            "secret": turnstile_secret,
            "response": data.turnstile_token,
            "remoteip": request.client.host if request.client else None
        }
        try:
            cf_response = requests.post(verify_url, data=payload, timeout=5)
            result = cf_response.json()
            
            if not result.get("success"):
                raise HTTPException(
                    status_code=400, 
                    detail="invalid_turnstile_token"
                )
        except requests.RequestException:
            raise HTTPException(
                status_code=503, 
                detail="turnstile_verification_service_unavailable"
            )
    
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
    client_ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")
    
    usuario = usuario_service.login(
        email = data.email, 
        password = data.password, 
        ip_address = client_ip, 
        user_agent=user_agent
    )

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
    
    client_ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")
    
    try:
        return auth_service.reset_password(
            token=data.token, 
            new_password=data.new_password,
            ip_address=client_ip,
            user_agent=user_agent
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
