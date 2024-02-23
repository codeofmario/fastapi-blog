from typing import Union

from pydantic import BaseModel

from app.enums.sort_direction import SortDirection


class TableFilterRequestDto(BaseModel):
    search: str = ''
    page: int = 0
    size: int = 10
    sortBy: Union[str, None] = None
    sortDirection: Union[SortDirection, None] = None
    all: bool = False

