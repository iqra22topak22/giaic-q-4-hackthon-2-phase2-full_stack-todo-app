from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class UserBase(SQLModel):
    email: str = Field(sa_column_kwargs={"unique": True, "nullable": False})
    username: str = Field(sa_column_kwargs={"unique": True, "nullable": False})

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str = Field(sa_column_kwargs={"nullable": False})
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(UserBase):
    password: str

class UserUpdate(SQLModel):
    email: Optional[str] = Field(default=None)
    username: Optional[str] = Field(default=None)
    is_active: Optional[bool] = Field(default=None)

class UserPublic(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime