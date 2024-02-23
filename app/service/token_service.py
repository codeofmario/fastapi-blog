from datetime import datetime, timedelta
from typing import List

from fastapi import Depends
import jwt

from app.config.settings import Settings, get_settings
from app.repository.token_repository import TokenRepository


class TokenService:
    def __init__(self, repository: TokenRepository = Depends(TokenRepository),
                 settings: Settings = Depends(get_settings)):
        self.repository = repository
        self.settings = settings

    async def get_access_token(self, user_id: str, token_id: str) -> str:
        return await self.repository.get(f"{user_id}.{token_id}.at")

    async def get_refresh_token(self, user_id: str, token_id: str) -> str:
        return await self.repository.get(f"{user_id}.{token_id}.rt")

    async def save_access_token(self, user_id: str, token_id: str, token: str) -> bool:
        return await self.repository.save(f"{user_id}.{token_id}.at", token, 15 * 60)

    async def save_refresh_token(self, user_id: str, token_id: str, token: str) -> bool:
        return await self.repository.save(f"{user_id}.{token_id}.rt", token, 7 * 24 * 60 * 60)

    async def delete_access_tokens(self, user_id: str, token_id: str) -> bool:
        return await self.repository.delete(f"{user_id}.{token_id}.at")

    async def delete_refresh_tokens(self, user_id: str, token_id: str) -> bool:
        return await self.repository.delete(f"{user_id}.{token_id}.rt")

    def generate_access_token(self, user_id: str, token_id: str, roles: List[str]) -> str:
        secret = self.settings.at_secret
        payload = {
            "exp": (datetime.now() + timedelta(minutes=15)).timestamp(),
            "sub": user_id,
            "tokenId": token_id,
            "roles": roles
        }
        return jwt.encode(payload, secret, algorithm="HS256")

    def generate_refresh_token(self, user_id: str, token_id: str, roles: List[str]) -> str:
        secret = self.settings.rt_secret
        payload = {
            "exp": (datetime.now() + timedelta(minutes=7 * 24 * 60)).timestamp(),
            "sub": user_id,
            "tokenId": token_id,
            "roles": roles
        }
        return jwt.encode(payload, secret, algorithm="HS256")


