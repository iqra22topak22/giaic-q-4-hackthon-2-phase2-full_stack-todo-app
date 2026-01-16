from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: str


class UserRegister(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool