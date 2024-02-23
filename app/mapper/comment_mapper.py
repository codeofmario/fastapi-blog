from app.dto.request.comment import CommentUpdateRequestDTO, CommentCreateRequestDTO
from app.dto.response.comment import CommentResponseDTO
from app.model.comment import Comment


class CommentMapper:
    @staticmethod
    def to_model(dto: CommentCreateRequestDTO) -> Comment:
        return Comment(
            body=dto.body,
            post_id=dto.post_id,
        )

    @staticmethod
    def to_dto(model: Comment) -> CommentResponseDTO:
        return CommentResponseDTO(
            id=str(model.id),
            body=model.body,
            user_id=str(model.user_id),
            post_id=str(model.post_id),
            created_at=model.created_at.isoformat(),
            updated_at=model.updated_at.isoformat(),
        )

    @staticmethod
    def to_update_model(model: Comment, dto: CommentUpdateRequestDTO) -> Comment:
        model.body = dto.body
        return model
