from typing import List

from pydantic import BaseModel, EmailStr


class CreateUserRequestDto(BaseModel):
    username: str
    email: EmailStr
    password: str
    passwordConfirm: str
    isActive: bool
    roleIds: List[str] = []

class UpdateUserRequestDto(BaseModel):
    id: str
    isActive: bool
    roleIds: List[str] = []
