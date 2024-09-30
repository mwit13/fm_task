from typing import Optional

from sqlalchemy import UniqueConstraint
from sqlmodel import Field
from pydantic import field_validator

from models.schemas.stg import STGSQLModel


class STGDayRevenue(STGSQLModel, table=True):
    __tablename__ = "stg_revenues_per_day"

    id: Optional[str]
    date: str = Field(primary_key=True)
    title: str = Field(primary_key=True)
    revenue: Optional[int] 
    theaters: Optional[int]
    distributor: Optional[str]

    __table_args__ = (UniqueConstraint('id', 'date', name='uix_id_date'),)

    @classmethod
    @field_validator('revenue', 'theaters', mode='before')
    def cast_to_int(cls, value):
        try:
            return int(value)
        except ValueError:
            return value

    @classmethod
    def get_trigger_name(cls) -> str:
        return f'trigger_update_modified_date_{cls.__tablename__}'

    @classmethod
    def get_trigger_sql(cls) -> str:
        modified_date = 'modified_date'
        primary_key = 'date'
        primary_key2 = 'title'
        return f"""
                CREATE TRIGGER {cls.get_trigger_name()}
                AFTER UPDATE ON {cls.__tablename__}
                FOR EACH ROW
                BEGIN
                    UPDATE {cls.__tablename__}
                    SET {modified_date} = CURRENT_TIMESTAMP
                    WHERE {primary_key} = OLD.{primary_key}
                    AND {primary_key2} = OLD.{primary_key2};
                END;
            """
