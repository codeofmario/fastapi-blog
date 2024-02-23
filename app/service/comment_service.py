from typing import List, Type

from fastapi import Depends

from app.dto.request.table_filter import TableFilterRequestDto
from app.dto.response.pagination import PaginationResponseDto
from app.model.comment import Comment
from app.repository.comment_repository import CommentRepository


class CommentService:
    def __init__(self, repository: CommentRepository = Depends(CommentRepository)):
        self.repository = repository

    def all(self) -> List[Type[Comment]]:
        return self.repository.all()

    def all_pageable(self, pageable: TableFilterRequestDto) -> (List[Type[Comment]], PaginationResponseDto):
        return self.repository.all_pageable(pageable)

    def one(self, id: int) -> Type[Comment] | None:
        return self.repository.one(id)

    def create(self, model: Comment) -> Comment:
        return self.repository.create(model)

    def update(self, model: Comment) -> Comment:
        return self.repository.update(model)

    def delete(self, model: Comment) -> None:
        return self.repository.delete(model)
