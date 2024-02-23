from typing import List, Type

from fastapi import Depends

from app.dto.request.table_filter import TableFilterRequestDto
from app.dto.response.pagination import PaginationResponseDto
from app.model.post import Post
from app.repository.post_repository import PostRepository


class PostService:
    def __init__(self, repository: PostRepository = Depends(PostRepository)):
        self.repository = repository

    def all(self) -> List[Type[Post]]:
        return self.repository.all()

    def all_pageable(self, pageable: TableFilterRequestDto) -> (List[Type[Post]], PaginationResponseDto):
        return self.repository.all_pageable(pageable)

    def one(self, id: str) -> Type[Post] | None:
        return self.repository.one(id)

    def create(self, model: Post) -> Post:
        return self.repository.create(model)

    def update(self, model: Post) -> Post:
        return self.repository.update(model)

    def delete(self, model: Post) -> None:
        return self.repository.delete(model)
