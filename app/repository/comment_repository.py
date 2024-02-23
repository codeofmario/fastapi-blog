from math import ceil
from typing import List, Type

from fastapi import Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.dto.request.table_filter import TableFilterRequestDto
from app.dto.response.pagination import PaginationResponseDto
from app.model.comment import Comment


class CommentRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def all(self) -> List[Type[Comment]]:
        return self.db.query(Comment).group_by(Comment.id).all()

    def all_pageable(self, pageable: TableFilterRequestDto) -> (List[Type[Comment]], PaginationResponseDto):
        count = self.db.query(Comment).count()
        data = self.db.query(Comment).group_by(Comment.id) \
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

    def one(self, id: str) -> Type[Comment] | None:
        return self.db.query(Comment).filter(Comment.id == id).first()

    def create(self, model: Comment) -> Comment:
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model

    def update(self, model: Comment) -> Comment:
        self.db.commit()
        self.db.refresh(model)
        return model

    def delete(self, model: Comment) -> None:
        self.db.delete(model)
        self.db.commit()
