from pydantic import BaseModel


class RoleResponseDto(BaseModel):
    id: str
    name: str
