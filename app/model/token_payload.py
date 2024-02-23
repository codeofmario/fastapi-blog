from typing import List

from pydantic import BaseModel


class TokenPayload(BaseModel):
    exp: int
    sub: str
    tokenId: str
    roles: List[str]
