from typing import List, Type

from fastapi import Depends

from app.dto.request.table_filter import TableFilterRequestDto
from app.dto.response.pagination import PaginationResponseDto
from app.model.user import User
from app.repository.user_repository import UserRepository


class UserService:
    def __init__(self, repository: UserRepository = Depends(UserRepository)):
        self.repository = repository

    def all(self) -> List[User]:
        return self.repository.all()

    def all_pageable(self, pageable: TableFilterRequestDto) -> (List[User], PaginationResponseDto):
        return self.repository.all_pageable(pageable)

    def one(self, id: str) -> Type[User]:
        return self.repository.one_by_id(id)

    def one_by_username(self, username: str) -> Type[User]:
        return self.repository.one_by_username(username)

    def one_by_email(self, email: str) -> Type[User]:
        return self.repository.one_by_email(email)

    def create(self, data: User) -> User:
        return self.repository.create(data)

    def update(self, data: User) -> User:
        return self.repository.update(data)

    def delete_by_id(self, id: str) -> None:
        return self.repository.delete_by_id(id)

    def find_all_by_id_in(self, ids: List[str]) -> List[Type[User]]:
        return self.repository.all_by_id_in(ids)
