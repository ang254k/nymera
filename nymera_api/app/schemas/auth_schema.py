from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    nombre: str
    email: EmailStr
    password: str
    turnstile_token: str
    lang: str = "es"
    
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
class ForgotPasswordRequest(BaseModel):
    email: EmailStr
    lang: str = "es"
    
class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str 
    
class VerifyEmailRequest(BaseModel):
    token: str
    
class ResendVerificationRequest(BaseModel):
    email: EmailStr
    lang: str = "es"