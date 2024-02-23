from pydantic import BaseModel


class CommentCreateRequestDTO(BaseModel):
    body: str
    post_id: str


class CommentUpdateRequestDTO(BaseModel):
    body: str
