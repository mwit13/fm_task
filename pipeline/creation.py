from sqlalchemy import Engine, text
from sqlmodel import Session, SQLModel

from models.schemas.dwh import DWHSQLModel
from models.schemas.stg import STGSQLModel
from pipeline import State


def create_from_orms(models: list[DWHSQLModel | STGSQLModel | SQLModel], engine: Engine):
    """
    Creates database tables for a list of ORM models and optionally sets up triggers.

    :param models: A list of ORM models (subclasses of `SQLModel`) for which to create tables.
    :type models: list[DWHSQLModel | STGSQLModel | SQLModel]
    :param engine: A SQLAlchemy engine used to connect to the database.
    :type engine: Engine

    :return: Returns `State.SUCCESS` if all tables and triggers are created successfully.
    :rtype: State

    :raises SQLAlchemyError: If there is an error creating the tables or triggers in the database.
    """

    for model in models:
        model.__table__.create(engine, checkfirst=True)
        msg: str = f"If not existed, table '{model.__tablename__}' created"

        if hasattr(model, 'get_trigger_name'):
            with Session(engine) as session:
                result = session.execute(text("""
                    SELECT name FROM sqlite_master WHERE type='trigger' AND name=:trigger_name;
                """), {"trigger_name": model.get_trigger_name()})
                if not result.fetchone():
                    session.execute(text(model.get_trigger_sql()))
                    session.commit()
                msg = msg + " + modified_date trigger"
        print(msg)

    return State.SUCCESS
