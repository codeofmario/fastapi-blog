from typing import TypeVar, Generic, List

from pydantic import BaseModel

T = TypeVar('T')


class PaginationResponseDto(BaseModel):
    pageNumber: int
    totalElements: int
    totalPages: int
    size: str


class PaginatedResponseDto(BaseModel, Generic[T]):
    data: List[T]
    pagination: PaginationResponseDto
