from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from starlette import status

from app.config.settings import get_settings, Settings
from app.model.token_payload import TokenPayload


def current_user_id(
        settings: Settings = Depends(get_settings),
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
) -> str:
    try:
        payload = jwt.decode(
            credentials.credentials, settings.at_secret, algorithms=["HS256"]
        )
        payload = TokenPayload(**payload)
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid user.",
        )

    return payload.sub


def current_user_role(role: str):
    def check_role(
            settings: Settings = Depends(get_settings),
            credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
    ) -> bool:
        try:
            payload = jwt.decode(
                credentials.credentials, settings.at_secret, algorithms=["HS256"]
            )
            payload = TokenPayload(**payload)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid user.",
            )

        if role not in payload.roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid role.",
            )

        return True

    return check_role


def current_user(
        settings: Settings = Depends(get_settings),
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
) -> TokenPayload:
    try:
        payload = jwt.decode(
            credentials.credentials, settings.at_secret, algorithms=["HS256"]
        )
        return TokenPayload(**payload)
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid user.",
        )


def current_user_refresh(
        settings: Settings = Depends(get_settings),
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
) -> TokenPayload:
    try:
        payload = jwt.decode(
            credentials.credentials, settings.rt_secret, algorithms=["HS256"]
        )
        return TokenPayload(**payload)
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid user.",
        )
