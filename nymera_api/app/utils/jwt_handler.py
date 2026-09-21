from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

from app.config import settings

def create_access_token(data:dict):
    payload = data.copy()
    
    expire = datetime.now(timezone.utc) + timedelta(minutes = settings.JWT_EXPIRE_MINUTES)
    
    payload["exp"] = expire
    
    token = jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm = settings.JWT_ALGORITHM
    )
    
    return token

def decode_token(token:str):
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        return None