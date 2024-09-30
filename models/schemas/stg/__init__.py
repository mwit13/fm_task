from abc import ABC, abstractmethod

from pydantic import ConfigDict
from sqlalchemy import text
from sqlmodel import SQLModel, Field

from models.definitions.objects import DateValue


class STGSQLModel(SQLModel, ABC):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    created_date: DateValue = Field(sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP"), })
    modified_date: DateValue = Field(sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP"), })

    @classmethod
    @abstractmethod
    def get_trigger_name(cls) -> str:
        ...

    @classmethod
    @abstractmethod
    def get_trigger_sql(cls) -> str:
        ...
