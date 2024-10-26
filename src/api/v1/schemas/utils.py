from typing import Type, TypeVar
from pydantic import BaseModel

from src.core.database.models.base import Base

T = TypeVar('T', bound=BaseModel)


# Utility function to convert SQLAlchemy objects to Pydantic models.
def to_pydantic(db_object: Base, pydantic_model: Type[T]) -> T:
    return pydantic_model(**db_object.__dict__)


def without_none_fields(pydantic_model: Type[T]) -> dict:
    dumped = pydantic_model.model_dump()
    for field in list(dumped.keys()):
        if dumped[field] is None:
            dumped.pop(field)
    return dumped
