from typing import Optional

from pydantic import ConfigDict
from sqlalchemy import text
from sqlmodel import Field, SQLModel

from models.definitions.objects import DateValue, IdInt


class DWHSQLModel(SQLModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: Optional[IdInt] = Field(default=None, primary_key=True)
    created_date: DateValue = Field(sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP"), })
    modified_date: DateValue = Field(sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP"), })

    @classmethod
    def get_trigger_name(cls):
        return f'trigger_update_modified_date_{cls.__tablename__}'

    @classmethod
    def get_trigger_sql(cls):
        modified_date = 'modified_date'
        primary_key = 'id'
        return f"""
                CREATE TRIGGER {cls.get_trigger_name()}
                AFTER UPDATE ON {cls.__tablename__}
                FOR EACH ROW
                BEGIN
                    UPDATE {cls.__tablename__}
                    SET {modified_date} = CURRENT_TIMESTAMP
                    WHERE {primary_key} = OLD.{primary_key};
                END;
            """
