from datetime import datetime
from typing import Literal
from uuid import UUID
from pydantic import BaseModel,EmailStr,Field

class UserRegister(BaseModel):
    full_name : str = Field(
        min_length = 3,
        max_length = 100
    )
    email: EmailStr
    password : str = Field(
        min_length = 8,
        max_length = 128
    )
class UserLogin(BaseModel):
    email : EmailStr
    password:str=Field(
        min_length=8,
        max_length = 128
    )


class UserResponse(BaseModel):
    id : UUID
    full_name:str
    email:EmailStr
    role: Literal["user","admin"]
    is_active:bool
    created_at:datetime

class UserActionResponse(BaseModel):
    message : str
    user : UserResponse


class TokenResponse(BaseModel):
    access_token:str
    token_type:str