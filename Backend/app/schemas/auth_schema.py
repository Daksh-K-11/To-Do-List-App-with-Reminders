from pydantic import BaseModel, EmailStr
from typing import Optional
    
class Login(BaseModel):
    email: EmailStr
    password : str
    
class ChangePassword(BaseModel):
    current_password: str
    new_password: str

class Token(BaseModel):
    access_token : str
    token_type : str
    
class TokenData(BaseModel):
    id : Optional[int] = None