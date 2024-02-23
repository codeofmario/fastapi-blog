from typing import Union, TypeVar, Generic

from pydantic import BaseModel

T = TypeVar('T')


class ErrorResponseDto(BaseModel, Generic[T]):
    timestamp: int
    message: str
    errors: Union[T, None]
