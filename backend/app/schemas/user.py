from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    full_name: Annotated[str, Field(min_length=2, max_length=30)]
    username: Annotated[str, Field(min_length=2, max_length=20, pattern=r"^[a-z0-9]+$")]
    email: Annotated[EmailStr, Field()]
    user_type: Annotated[str, Field(default="0")]


class UserRead(UserBase):
    id: int
    created_at: datetime
    roles: Annotated[list[str], Field(default=None)]


class UserCreate(UserBase):
    model_config = ConfigDict(extra="forbid")

    password: Annotated[str, Field(pattern=r"^.{8,}|[0-9]+|[A-Z]+|[a-z]+|[^a-zA-Z0-9]+$")]
    roles: Annotated[list[int], Field()]


class UserUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: int
    full_name: Annotated[str, Field(min_length=2, max_length=30, default=None)]
    username: Annotated[ str, Field(min_length=2, max_length=20, pattern=r"^[a-z0-9]+$", default=None)]
