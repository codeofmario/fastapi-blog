from app.dto.request.post import PostCreateRequestDTO, PostUpdateRequestDTO
from app.dto.response.post import PostResponseDTO
from app.model.post import Post


class PostMapper:
    @staticmethod
    def to_model(dto: PostCreateRequestDTO) -> Post:
        return Post(
            title=dto.title,
            body=dto.body,
        )

    @staticmethod
    def to_dto(model: Post) -> PostResponseDTO:
        return PostResponseDTO(
            id=str(model.id),
            title=model.title,
            body=model.body,
            user_id=str(model.user_id),
            created_at=model.created_at.isoformat(),
            updated_at=model.updated_at.isoformat(),
        )

    @staticmethod
    def to_update_model(model: Post, dto: PostUpdateRequestDTO) -> Post:
        model.title = dto.title
        model.body = dto.body
        return model
