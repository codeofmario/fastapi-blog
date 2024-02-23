from math import ceil
from typing import List, Type

from fastapi import Depends, HTTPException
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.dto.request.table_filter import TableFilterRequestDto
from app.dto.response.pagination import PaginationResponseDto
from app.enums.sort_direction import SortDirection
from app.model.role import Role


class RoleRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def all(self) -> (List[Type[Role]], PaginationResponseDto):
        return self.db.query(Role).group_by(Role.id).all()

    def all_pageable(self, pageable: TableFilterRequestDto):
        count = self.db.query(Role).count()
        sort_by = pageable.sortBy if pageable.sortBy else "name"
        sort = asc(sort_by) if pageable.sortDirection == SortDirection.asc else desc(sort_by)
        data = self.db.query(Role).group_by(Role.id) \
            .filter(Role.name.contains(pageable.search)) \
            .order_by(sort) \
            .limit(pageable.size) \
            .offset(pageable.page * pageable.size) \
            .all()
        pagination = PaginationResponseDto(
            pageNumber=pageable.page,
            totalElements=count,
            totalPages=ceil(count/pageable.size),
            size=pageable.size
        )
        return data, pagination

    def one_by_id(self, id: str) -> Type[Role]:
        user = self.db.query(Role).filter(Role.id == id).first()
        if not user:
            raise HTTPException(status_code=404,
                                detail=f"Role with id: {id} was not found")
        return user

    def all_by_id_in(self, ids: List[str]) -> List[Type[Role]]:
        return self.db.query(Role).filter(Role.id.in_(ids)).all()

    def create(self, model: Role) -> Role:
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model

    def update(self, model: Role) -> Role:
        self.db.query(Role).filter(Role.id == model.id).update(model)
        self.db.commit()
        return model

    def delete_by_id(self, id: str) -> None:
        user = self.one_by_id(id)
        user.delete()
        self.db.commit()
