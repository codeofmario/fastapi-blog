from pydantic import BaseModel


class CommentResponseDTO(BaseModel):
    id: str
    body: str
    user_id: str
    post_id: str
    updated_at: str
    created_at: str
