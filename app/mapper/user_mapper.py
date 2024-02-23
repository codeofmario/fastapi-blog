from app.dto.request.user import CreateUserRequestDto, UpdateUserRequestDto
from app.dto.response.role import RoleResponseDto
from app.dto.response.user import UserResponseDto
from app.model.user import User


class UserMapper:
    def to_model(self, dto: CreateUserRequestDto) -> User:
        return User(
            username=dto.username,
            email=dto.email,
            is_active=dto.isActive,
        )

    def to_update_model(self, dto: UpdateUserRequestDto) -> User:
        return User(
            id=dto.id,
            is_active=dto.isActive,
        )

    def to_dto(self, model: User) -> UserResponseDto:
        return UserResponseDto(
            id=str(model.id),
            username=model.username,
            email=model.email,
            isActive=model.is_active,
            avatarUrl=f"http://localhost:8400/fastapiblog/{model.avatar_id}",
            roles=[RoleResponseDto(id=str(role.id), name=role.name) for role in model.roles]
        )
