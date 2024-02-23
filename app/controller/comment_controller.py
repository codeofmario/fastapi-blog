from fastapi import APIRouter, Depends
from starlette import status

from app.dto.request.comment import CommentCreateRequestDTO, CommentUpdateRequestDTO
from app.dto.request.table_filter import TableFilterRequestDto
from app.dto.response.comment import CommentResponseDTO
from app.dto.response.pagination import PaginatedResponseDto
from app.mapper.comment_mapper import CommentMapper
from app.service.comment_service import CommentService
from app.util.current_user_util import current_user_id, current_user

router = APIRouter(prefix="/comments", tags=["comments"], dependencies=[Depends(current_user)])

@router.get("/", response_model=PaginatedResponseDto[CommentResponseDTO])
def find_all(pageable: TableFilterRequestDto = Depends(), service: CommentService = Depends(CommentService),
             mapper: CommentMapper = Depends(CommentMapper)):
    data, pagination = service.all_pageable(pageable)

    return PaginatedResponseDto(
        data=[mapper.to_dto(user) for user in data],
        pagination=pagination
    )


@router.post("/", response_model=CommentResponseDTO)
async def create(dto: CommentCreateRequestDTO, service: CommentService = Depends(),
                 user_id: str = Depends(current_user_id)):
    model = CommentMapper.to_model(dto)
    model.user_id = user_id
    model = service.create(model)
    return CommentMapper.to_dto(model)


@router.get("/{id}", response_model=CommentResponseDTO)
async def get(id: str, service: CommentService = Depends()):
    model = service.one(id)
    return CommentMapper.to_dto(model)


@router.put("/{id}", response_model=CommentResponseDTO)
async def update(id: str, dto: CommentUpdateRequestDTO, service: CommentService = Depends(CommentService)):
    model = service.one(id)
    model = CommentMapper.to_update_model(model, dto)
    model = service.update(model)
    return CommentMapper.to_dto(model)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: str, service: CommentService = Depends()):
    model = service.one(id)
    service.delete(model)
