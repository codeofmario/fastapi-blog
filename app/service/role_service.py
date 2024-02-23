from typing import List, Type

from fastapi import Depends

from app.dto.request.table_filter import TableFilterRequestDto
from app.dto.response.pagination import PaginationResponseDto
from app.model.role import Role
from app.repository.role_repository import RoleRepository


class RoleService:
    def __init__(self, repository: RoleRepository = Depends(RoleRepository)):
        self.repository = repository

    def all(self) -> List[Role]:
        return self.repository.all()

    def all_pageable(self, pageable: TableFilterRequestDto) -> (List[Role], PaginationResponseDto):
        return self.repository.all_pageable(pageable)

    def one(self, id: str) -> Type[Role]:
        return self.repository.one_by_id(id)

    def create(self, model: Role) -> Role:
        return self.repository.create(model)

    def update(self, model: Role) -> Role:
        return self.repository.update(model)

    def delete_by_id(self, id: str) -> None:
        return self.repository.delete_by_id(id)

    def find_all_by_id_in(self, ids: List[str]) -> List[Type[Role]]:
        return self.repository.all_by_id_in(ids)
