from sqlalchemy import Column, JSON
from sqlmodel import Field

from models.definitions.objects import Title, JSONDict
from models.schemas.stg import STGSQLModel


class STGMovie(STGSQLModel, table=True):
    __tablename__ = "stg_movies_details"

    title: Title = Field(primary_key=True)
    response: JSONDict = Field(sa_column=Column(JSON, nullable=False))

    @classmethod
    def get_trigger_name(cls) -> str:
        return f'trigger_update_modified_date_{cls.__tablename__}'

    @classmethod
    def get_trigger_sql(cls) -> str:
        modified_date = 'modified_date'
        primary_key = 'title'
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
