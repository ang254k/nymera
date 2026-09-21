from pydantic import BaseModel, EmailStr, Field
#Peticiones

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    nombre: str = Field(min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6)
    
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
class ForgotPasswordRequest(BaseModel):
    email: EmailStr
    
class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(min_length=8)