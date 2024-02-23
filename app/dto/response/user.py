from typing import Union, List

from pydantic import BaseModel

from app.dto.response.role import RoleResponseDto


class UserInfoResponseDto(BaseModel):
    id: str
    username: str
    email: str
    avatarUrl: Union[str, None] = None


class UserResponseDto(BaseModel):
    id: str
    username: str
    email: str
    isActive: str
    avatarUrl: Union[str, None]
    roles: List[RoleResponseDto]
