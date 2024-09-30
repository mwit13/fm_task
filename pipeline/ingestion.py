import json
import os
from dataclasses import dataclass
from typing import Type

import requests
import pandas as pd
from furl import furl
from requests import Response

from sqlalchemy import Engine, select, text
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy.sql.operators import is_
from sqlmodel import SQLModel
from tqdm import tqdm

from models.definitions.objects import Title
from models.schemas.stg.movies_details import STGMovie
from models.schemas.stg.revenue_per_day import STGDayRevenue
from pipeline import State


@dataclass
class CSVIngesterDefinition:
    filepath: str
    orm_class: declarative_base
    separator: str = ','
    is_header: bool = True


@dataclass
class OMDBAPIFetchDefinition:
    omdb_address: str = 'http://www.omdbapi.com'
    api_key: str = os.environ.get('OMDB_API_KEY')
    allowed_failed_attempts: int = 3
    dry_run: bool = False


def csv_ingester_any_orm(definition: CSVIngesterDefinition,
                         engine: Engine):
    """
    Reads a CSV file and ingests its data into a database using the provided ORM model.

    :param definition: An object containing the CSV file path, separator, header
                       information, and the ORM used for database operations.
    :type definition: CSVIngesterDefinition
    :param engine: A SQLAlchemy engine used to connect to the database.
    :type engine: Engine

    :return: Returns `State.SUCCESS` if the CSV ingestion and database commit are successful.
    :rtype: State

    :raises ValueError: If the CSV file format is invalid or if the ORM class instantiation fails.
    :raises SQLAlchemyError: If there is an error merging the data into the database.
    """
    df = pd.read_csv(filepath_or_buffer=definition.filepath,
                     sep=definition.separator,
                     header=0 if definition.is_header else None,
                     skipinitialspace=True,
                     skip_blank_lines=True,
                     parse_dates=False)

    print("CSV loaded to memory. Starting db merge")

    with Session(engine) as session:
        for index, row in tqdm(df.iterrows()):
            session.merge(definition.orm_class(**row))
        session.commit()

    return State.SUCCESS


def fetch_movies_details(definition: OMDBAPIFetchDefinition,
                         api_key: str,
                         engine: Engine,
                         limit_calls: int | None = None):
    """
    Fetches movie details from the OMDB API and updates the database with the results.

    This function retrieves a list of distinct movie titles from the database, queries the OMDB API for
    details. Data is merged into the proper table

    :param limit_calls: To limit artificially the execution.
    :param definition: Configuration for the OMDB API fetch process,
     including API address, allowed failed attempts, and dry run option.
    :type definition: OMDBAPIFetchDefinition
    :param api_key: The API key used to authenticate with the OMDB API.
    :type api_key: str
    :param engine: A SQLAlchemy engine used to connect to the database.
    :type engine: Engine

    :return: Returns `State.SUCCESS` if the API fetch and database merge are successful.
    :rtype: State

    :raises ValueError: If the API key is not provided.
    :raises SQLAlchemyError: If there is an error executing the SQL operations.
    :raises Exception: For any other unexpected errors during API fetching or database interaction.
    """
    if not api_key:
        raise ValueError('API key not defined')

    _check_attribute(model=STGMovie, attr_name='title')
    _check_attribute(model=STGMovie, attr_name='response')
    _check_attribute(model=STGDayRevenue, attr_name='title')

    if not definition.dry_run:
        titles: tuple[Title, ...] = _get_distinct_not_present_titles(engine)
    else:
        titles: tuple[Title, ...] = _get_distinct_titles(engine)

    movie_details: list[dict] = []
    faulty_counter: int = 0
    msgs: list[str] = []

    for title in tqdm(titles):
        if faulty_counter > definition.allowed_failed_attempts:
            msgs.append(f"The number of faulty API responses exceeded the allowance. Finishing calling API")
            break
        try:
            omdb_response: Response | None = _get_omdb_data(definition.omdb_address, api_key, title)
            if not isinstance(omdb_response, Response):
                faulty_counter += 1
                msgs.append(f"Faulty API response for {title}.")
                continue
            else:
                response_json = omdb_response.json()
                if not eval(response_json.get('Response', 'None')):
                    if not response_json.get('Error', '') == 'Movie not found!':
                        faulty_counter += 1
                    msgs.append(f"Faulty API response for {title}. {response_json.get('Error', 'Error not known')}")
                    continue

            movie_details.append(dict(title=title, response=json.dumps(response_json)))

            no = len(movie_details)
            if limit_calls and no >= limit_calls:
                break

        except Exception as e:
            msgs.append(f"Error processing title {title}: {e}")

    for msg in msgs:
        print(msg)
    no = len(movie_details)
    if no:
        print(f"API calls finished. Fetched {no} entries. The db merge starts.")
    else:
        print(f"API calls finished. 0 entries fetched")
        return State.SUCCESS

    tmp_name = f"tmp_{STGMovie.__tablename__}"
    try:
        df = pd.DataFrame.from_dict(movie_details)
        df.to_sql(tmp_name, engine, schema=None, if_exists='replace', index=False, index_label=None, chunksize=None,
                  dtype=None, method=None)
    except Exception:
        raise

    with Session(engine) as session:
        try:
            session.execute(text(f"""
                INSERT INTO {STGMovie.__tablename__} (
                    title
                    ,response
                    )
                SELECT * 
                FROM (
                    SELECT title
                        ,response
                    FROM {tmp_name}
                    ) a
                WHERE 1 ON CONFLICT(title)
                DO UPDATE SET response = excluded.response
                WHERE response != excluded.response;
            """))
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    with Session(engine) as session:
        try:
            session.execute(text(f"DROP TABLE {tmp_name}"))
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    return State.SUCCESS


def csv_ingester_revenues(definition: CSVIngesterDefinition,
                          engine: Engine):
    """
    Reads a CSV file and ingests its data into a database only for STGDayRevenues ORM.
    Prepared for faster ingestion than csv_ingester_any_orm

    :param definition: An object containing the CSV file path, separator, header
                       information, and STGDayRevenues ORM.
    :type definition: CSVIngesterDefinition for STGDayRevenues ORM
    :param engine: A SQLAlchemy engine used to connect to the database.
    :type engine: Engine

    :return: Returns `State.SUCCESS` if the CSV ingestion and database commit are successful.
    :rtype: State

    :raises ValueError: If the CSV file format is invalid or if the ORM class instantiation fails.
    :raises SQLAlchemyError: If there is an error merging the data into the database.
    """
    tmp_name = f"tmp_{definition.orm_class.__tablename__}"

    df = pd.read_csv(filepath_or_buffer=definition.filepath,
                     sep=definition.separator,
                     header=0 if definition.is_header else None,
                     skipinitialspace=True,
                     skip_blank_lines=True,
                     parse_dates=False)

    print("CSV loaded to memory. Starting db merge")

    df.to_sql(tmp_name, engine, schema=None, if_exists='replace', index=False, index_label=None, chunksize=None,
              dtype=None, method=None)

    with Session(engine) as session:
        try:
            session.execute(text(f"""
                INSERT INTO {definition.orm_class.__tablename__} (
                    id
                    ,"date"
                    ,title
                    ,revenue
                    ,theaters
                    ,distributor
                    )
                SELECT *
                FROM (
                    SELECT id
                        ,"date"
                        ,title
                        ,CAST(revenue AS INT)
                        ,CAST(theaters AS INT)
                        ,distributor
                    FROM {tmp_name}
                    ) a
                WHERE 1 ON CONFLICT(id, "date")
                DO UPDATE SET title = excluded.title
                    ,revenue = excluded.revenue
                    ,theaters = excluded.theaters
                    ,distributor = excluded.distributor
                WHERE title != excluded.title
                    OR revenue != excluded.revenue
                    OR theaters != excluded.theaters
                    OR distributor != excluded.distributor;
            """))
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    with Session(engine) as session:
        try:
            session.execute(text(f"DROP TABLE {tmp_name}"))
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    return State.SUCCESS


def _get_distinct_titles(engine: Engine) -> tuple[Title, ...]:
    with Session(engine) as session:
        statement = select(STGDayRevenue.title).distinct()
        results = tuple(session.execute(statement).scalars().all())
        return results


def _get_distinct_not_present_titles(engine: Engine) -> tuple[Title, ...]:
    with Session(engine) as session:
        statement = (
            select(STGDayRevenue.title)
            .distinct()
            .outerjoin(STGMovie, STGDayRevenue.title == STGMovie.title)
            .where(is_(STGMovie.title, None))
        )
        results = tuple(session.execute(statement).scalars().all())
        return results


def _get_omdb_data(omdb_address: str, api_key: str, movie_title: Title) -> Response | None:
    url = furl(omdb_address).add(dict(apikey=api_key, t=movie_title)).url
    try:
        return requests.get(url)
    except Exception as e:
        print(e)
        return None


def _check_attribute(model: Type[SQLModel], attr_name: str):
    if not hasattr(model, attr_name):
        raise AttributeError(f"{model.__name__} has no attribute '{attr_name}'")
