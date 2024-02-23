from typing import List

from fastapi import Depends, APIRouter
from starlette import status

from app.dto.request.post import PostUpdateRequestDTO, PostCreateRequestDTO
from app.dto.request.table_filter import TableFilterRequestDto
from app.dto.response.pagination import PaginatedResponseDto
from app.dto.response.post import PostResponseDTO
from app.mapper.post_mapper import PostMapper
from app.service.post_service import PostService
from app.util.current_user_util import current_user_id, current_user

router = APIRouter(prefix="/posts", tags=["posts"], dependencies=[Depends(current_user)])


@router.get("/", response_model=PaginatedResponseDto[PostResponseDTO])
def find_all(pageable: TableFilterRequestDto = Depends(), service: PostService = Depends(PostService),
             mapper: PostMapper = Depends(PostMapper)):
    data, pagination = service.all_pageable(pageable)

    return PaginatedResponseDto(
        data=[mapper.to_dto(user) for user in data],
        pagination=pagination
    )


@router.post("/", response_model=PostResponseDTO)
async def create(dto: PostCreateRequestDTO, service: PostService = Depends(),
                 user_id: str = Depends(current_user_id)):
    model = PostMapper.to_model(dto)
    model.user_id = user_id
    model = service.create(model)
    return PostMapper.to_dto(model)


@router.get("/{id}", response_model=PostResponseDTO)
async def get(id: str, service: PostService = Depends()):
    model = service.one(id)
    return PostMapper.to_dto(model)


@router.put("/{id}", response_model=PostResponseDTO)
async def update(id: str, dto: PostUpdateRequestDTO,
                 service: PostService = Depends(PostService)):
    model = service.one(id)
    model = PostMapper.to_update_model(model, dto)
    model = service.update(model)
    return PostMapper.to_dto(model)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: str, service: PostService = Depends()):
    model = service.one(id)
    service.delete(model)
