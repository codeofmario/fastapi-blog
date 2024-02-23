from typing import Union

import bcrypt
from fastapi import APIRouter, UploadFile, File, Depends
from starlette import status

from app.dto.request.table_filter import TableFilterRequestDto
from app.dto.request.user import CreateUserRequestDto, UpdateUserRequestDto
from app.dto.response.pagination import PaginatedResponseDto
from app.dto.response.user import UserResponseDto
from app.mapper.user_mapper import UserMapper
from app.service.role_service import RoleService
from app.service.store_service import StoreService
from app.service.user_service import UserService
from app.util.current_user_util import current_user_id, current_user_role

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(current_user_role("ROLE_ADMIN"))]
)


@router.get("/", response_model=PaginatedResponseDto[UserResponseDto])
def find_all(pageable: TableFilterRequestDto = Depends(), service: UserService = Depends(UserService),
             mapper: UserMapper = Depends(UserMapper)):
    data, pagination = service.all_pageable(pageable)

    return PaginatedResponseDto(
        data=[mapper.to_dto(user) for user in data],
        pagination=pagination
    )


@router.post("/", response_model=UserResponseDto)
async def create(dto: CreateUserRequestDto,
                 mapper: UserMapper = Depends(UserMapper),
                 user_service: UserService = Depends(UserService),
                 role_service: RoleService = Depends(RoleService)):
    model = mapper.to_model(dto)

    model.password = bcrypt.hashpw(dto.password.encode('utf-8'), bcrypt.gensalt())
    model.roles = role_service.find_all_by_id_in(dto.roleIds)
    model = user_service.create(model)

    return mapper.to_dto(model)


@router.get("/{id}", response_model=UserResponseDto)
def one(id: str,
        mapper: UserMapper = Depends(UserMapper),
        user_service: UserService = Depends(UserService)):
    model = user_service.one(id)

    return mapper.to_dto(model)


@router.put("/{id}", response_model=UserResponseDto)
async def update(id: str,
                 dto: UpdateUserRequestDto,
                 mapper: UserMapper = Depends(UserMapper),
                 user_service: UserService = Depends(UserService),
                 role_service: RoleService = Depends(RoleService)):
    model = user_service.one(id)
    model.is_active = dto.isActive
    model.roles = role_service.find_all_by_id_in(dto.roleIds)
    model = user_service.update(model)

    return mapper.to_dto(model)


@router.put("/{id}/avatar", response_model=UserResponseDto)
async def avatar(id: str,
                 avatar: Union[UploadFile, None] = File(default=None),
                 mapper: UserMapper = Depends(UserMapper),
                 store_service: StoreService = Depends(StoreService),
                 user_service: UserService = Depends(UserService)):
    model = user_service.one(id)

    if avatar and model.avatar_id:
        store_service.delete(model.avatar_id)

    if avatar:
        model.avatar_id = await store_service.save(avatar)

    model = user_service.update(model)

    return mapper.to_dto(model)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: str,
           store_service: StoreService = Depends(StoreService),
           user_service: UserService = Depends(UserService)):
    model = user_service.one(id)

    if model.avatar_id:
        store_service.delete(model.avatar_id)

    user_service.delete_by_id(id)
