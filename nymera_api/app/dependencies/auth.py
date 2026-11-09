from fastapi import Depends, HTTPException, status, Request

from app.utils.jwt_handler import decode_token
from app.repositories.usuario_repository import UsuarioRepository
from app.models.usuario import Usuario

repo = UsuarioRepository()

def get_current_user(request: Request) -> Usuario:
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "unauthorized"
    )
    token = request.cookies.get("access_token")
    
    if not token:
        raise credentials_exception
    
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception
    
    raw_usuario_id = payload.get("sub")
    if raw_usuario_id is None:
        raise credentials_exception
    
    try:
        usuario_id = int(raw_usuario_id)
    except(TypeError, ValueError):
        raise credentials_exception
    
    user = repo.get_by_id(usuario_id)
    if user is None:
        raise credentials_exception
    
    return user

def get_current_user_optional(request: Request) -> Usuario | None:
    token = request.cookies.get("access_token")
    if not token:
        return None
    
    payload = decode_token(token)
    if payload is None:
        return None
    
    raw_usuario_id = payload.get("sub")
    if raw_usuario_id is None:
        return None
    
    try:
        usuario_id = int(raw_usuario_id)
    except(TypeError, ValueError):
        return None
    
    user = repo.get_by_id(int(usuario_id))
    
    return user