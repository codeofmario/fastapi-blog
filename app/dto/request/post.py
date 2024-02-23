from pydantic import BaseModel


class PostCreateRequestDTO(BaseModel):
    title: str
    body: str


class PostUpdateRequestDTO(BaseModel):
    title: str
    body: str
