from math import ceil
from typing import List, Type

from fastapi import Depends, HTTPException
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session, joinedload

from app.config.database import get_db
from app.dto.request.table_filter import TableFilterRequestDto
from app.dto.response.pagination import PaginationResponseDto
from app.enums.sort_direction import SortDirection
from app.model.user import User


class UserRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def all(self) -> (List[Type[User]], PaginationResponseDto):
        return self.db.query(User).group_by(User.id).all()

    def all_pageable(self, pageable: TableFilterRequestDto):
        count = self.db.query(User).count()
        sort_by = pageable.sortBy if pageable.sortBy else "username"
        sort = asc(sort_by) if pageable.sortDirection == SortDirection.asc else desc(sort_by)
        data = self.db.query(User).group_by(User.id) \
            .filter(User.username.contains(pageable.search)) \
            .filter(User.email.contains(pageable.search)) \
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

    def one_by_id(self, id: str) -> Type[User]:
        user = self.db.query(User).options(joinedload(User.roles)).filter(User.id == id).first()
        if not user:
            raise HTTPException(status_code=404,
                                detail=f"User with id: {id} was not found")
        return user

    def one_by_username(self, username: str) -> Type[User]:
        user = self.db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=404,
                                detail=f"User with username: {username} was not found")
        return user

    def one_by_email(self, email: str) -> Type[User]:
        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404,
                                detail=f"User with username: {email} was not found")
        return user

    def all_by_id_in(self, ids: List[str]) -> List[Type[User]]:
        return self.db.query(User).filter(User.id.in_(ids)).all()

    def create(self, model: User) -> User:
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model

    def update(self, model: User) -> User:
        self.db.commit()
        self.db.refresh(model)
        return model

    def delete_by_id(self, id: str) -> None:
        self.db.query(User).filter(User.id == id).delete()
        self.db.commit()
