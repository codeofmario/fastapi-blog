from pydantic import BaseModel


class PostResponseDTO(BaseModel):
    id: str
    title: str
    body: str
    user_id: str
    updated_at: str
    created_at: str
