from sqlalchemy import text, Engine
from sqlalchemy.orm import Session

from pipeline import State


class SQLFilename(str):
    pass


def create_using_sql(filename: SQLFilename, engine: Engine) -> State:
    """
    Executes an SQL query from a file and applies the changes to a database.

    This function reads an SQL query from a file located in the
    `./pipeline/create_views/` directory, executes the query within a session
    using the provided SQLAlchemy engine. If the query is successful, it commits
    the transaction, otherwise it rolls back any changes and raises the exception.

    :param filename: The name of the SQL file (excluding the path) that contains the SQL query.
    :type filename: SQLFilename
    :param engine: A SQLAlchemy engine used to connect to the database.
    :type engine: Engine

    :return: Returns `State.SUCCESS` if the SQL execution and transaction commit are successful.
    :rtype: State

    :raises FileNotFoundError: If the specified file cannot be found or opened.
    :raises SQLAlchemyError: If there is an error executing the SQL query, it will raise the corresponding SQLAlchemy exception.
    :raises Exception: Any other unexpected errors during file handling or session execution.
    """

    directory = "./pipeline/create_views"
    try:
        with open(f'{directory}/{filename}', 'r') as file:
            sql_query = file.read()
    except FileNotFoundError:
        raise

    with Session(engine) as session:
        try:
            session.execute(text(sql_query))
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    return State.SUCCESS
