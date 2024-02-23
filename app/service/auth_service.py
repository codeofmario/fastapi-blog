import uuid
from typing import List

import bcrypt
from fastapi import Depends, HTTPException
from starlette import status

from app.config.settings import Settings, get_settings
from app.dto.request.login import LoginRequestDto
from app.dto.response.token import TokensResponseDto
from app.dto.response.user import UserInfoResponseDto
from app.service.role_service import RoleService
from app.service.store_service import StoreService
from app.service.token_service import TokenService
from app.service.user_service import UserService


class AuthService:
    def __init__(self,
                 settings: Settings = Depends(get_settings),
                 user_service: UserService = Depends(UserService),
                 role_service: RoleService = Depends(RoleService),
                 token_service: TokenService = Depends(TokenService),
                 store_service: StoreService = Depends(StoreService)):
        self.settings = settings
        self.user_service = user_service
        self.role_service = role_service
        self.token_service = token_service
        self.store_service = store_service

    async def login(self, dto: LoginRequestDto) -> TokensResponseDto:
        user = self.user_service.one_by_username(dto.username)

        if not user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f"Access Denied")

        password_matches = bcrypt.checkpw(dto.password.encode("utf-8"), user.password.encode("utf-8"))

        if not password_matches:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f"Access Denied")

        return await self.get_tokens(str(user.id), [role.name for role in user.roles])

    def logout(self, user_id: str, token_id: str) -> bool:
        self.delete_tokens(user_id, token_id)
        return True

    async def refresh_tokens(self, user_id: str, token_id: str) -> TokensResponseDto:
        user = self.user_service.one(user_id)

        refresh_token = self.token_service.get_refresh_token(user_id, token_id)
        if not user or not refresh_token:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f"Access Denied")

        await self.delete_tokens(user_id, token_id)
        return await self.get_tokens(str(user.id), [role.name for role in user.roles])

    def me(self, user_id: str) -> UserInfoResponseDto:
        user = self.user_service.one(user_id)

        return UserInfoResponseDto(
            id=str(user.id),
            username=user.username,
            email=user.email,
            avatarUrl=user.avatar_id
        )

    async def get_tokens(self, user_id: str, roles: List[str]) -> TokensResponseDto:
        token_id = str(uuid.uuid4())
        tokens = self.generate_tokens(user_id, token_id, roles)
        await self.save_tokens(user_id, token_id, tokens)
        return tokens

    def generate_tokens(self, user_id: str, token_id: str, roles: List[str]) -> TokensResponseDto:
        access_token = self.token_service.generate_access_token(user_id, token_id, roles)
        refresh_token = self.token_service.generate_refresh_token(user_id, token_id, roles)

        return TokensResponseDto(
            accessToken=access_token,
            refreshToken=refresh_token
        )

    async def save_tokens(self, user_id: str, token_id: str, tokens: TokensResponseDto):
        await self.token_service.save_access_token(user_id, token_id, tokens.accessToken)
        await self.token_service.save_refresh_token(user_id, token_id, tokens.refreshToken)

    async def delete_tokens(self, user_id: str, token_id: str):
        await self.token_service.delete_access_tokens(user_id, token_id)
        await self.token_service.delete_refresh_tokens(user_id, token_id)
