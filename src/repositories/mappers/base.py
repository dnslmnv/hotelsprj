from typing import TypeVar
from pydantic import BaseModel
from src.database import Base

SchemaType = TypeVar("SchemaType", bound=BaseModel)
DBModelType = TypeVar("DBModelType", bound=Base)


class DataMapper:
    db_model: type[DBModelType] = None
    schema: type[SchemaType] = None

    @classmethod
    def map_to_domain_entity(cls, data):
        return cls.schema.model_validate(data, from_attributes=True)

    # создает модель sql alchemy
    @classmethod
    def map_to_persistence_entity(cls, data):
        return cls.db_model(**data.model_dump())
