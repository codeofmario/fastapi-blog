from app.dto.response.user import UserInfoResponseDto
from app.model.user import User


class AuthMapper:
    def to_dto(self, model: User) -> UserInfoResponseDto:
        return UserInfoResponseDto(
            id=model.id,
            username=model.username,
            email=model.email,
            avatarUrl=f"http://localhost:8400/fastapiblog/{model.avatar_id}",
        )
