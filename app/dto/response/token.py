from pydantic import BaseModel


class TokensResponseDto(BaseModel):
    accessToken: str
    refreshToken: str

