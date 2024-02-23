from math import ceil
from typing import List, Type

from fastapi import Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.dto.request.table_filter import TableFilterRequestDto
from app.dto.response.pagination import PaginationResponseDto
from app.model.post import Post


class PostRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def all(self) -> List[Type[Post]]:
        return self.db.query(Post).group_by(Post.id).all()

    def all_pageable(self, pageable: TableFilterRequestDto) -> (List[Type[Post]], PaginationResponseDto):
        count = self.db.query(Post).count()
        data = self.db.query(Post).group_by(Post.id) \
            .limit(pageable.size) \
            .offset(pageable.page * pageable.size) \
            .all()

        pagination = PaginationResponseDto(
            pageNumber=pageable.page,
            totalElements=count,
            totalPages=ceil(count / pageable.size),
            size=pageable.size
        )
        return data, pagination

    def one(self, id: str) -> Type[Post] | None:
        return self.db.query(Post).filter(Post.id == id).first()

    def create(self, model: Post) -> Post:
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model

    def update(self, model: Post) -> Post:
        self.db.commit()
        self.db.refresh(model)
        return model

    def delete(self, model: Post) -> None:
        self.db.delete(model)
        self.db.commit()

