from fastapi import APIRouter, Depends
from starlette import status

from app.dto.request.login import LoginRequestDto
from app.dto.response.token import TokensResponseDto
from app.dto.response.user import UserInfoResponseDto
from app.model.token_payload import TokenPayload
from app.service.auth_service import AuthService
from app.util.current_user_util import current_user, current_user_refresh, current_user_id

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/signin", response_model=TokensResponseDto)
async def login(dto: LoginRequestDto, service: AuthService = Depends(AuthService)):
    return await service.login(dto)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(service: AuthService = Depends(AuthService),
           session_user: TokenPayload = Depends(current_user)):
    service.logout(session_user.sub, session_user.tokenId)


@router.post("/refresh", response_model=TokensResponseDto)
async def refresh_tokens(service: AuthService = Depends(AuthService),
                         session_user: TokenPayload = Depends(current_user_refresh)):
    return await service.refresh_tokens(session_user.sub, session_user.tokenId)


@router.get("/me", response_model=UserInfoResponseDto)
def me(service: AuthService = Depends(AuthService),
       user_id: str = Depends(current_user_id)):
    return service.me(user_id)
