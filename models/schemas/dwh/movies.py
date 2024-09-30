from typing import Optional

from sqlalchemy import Column, JSON, String
from sqlmodel import Field

from models.definitions.objects import Title, AgeRating, Genre, FullName, Description, Language, Country, \
    IMDbId, MovieType, DollarsFull, Company, IdInt
from models.schemas.dwh import DWHSQLModel


class DWHMovie(DWHSQLModel, table=True):
    __tablename__ = "dwh_dim__movies"

    title: Title = Field(nullable=False, index=True)
    start_year_date_id: Optional[IdInt] = Field(nullable=True, foreign_key="dwh_dim__dates.id", index=True)
    end_year_date_id: Optional[IdInt] = Field(nullable=True, foreign_key="dwh_dim__dates.id", index=True)
    rated: Optional[AgeRating]
    release_date_id: Optional[IdInt] = Field(nullable=True, foreign_key="dwh_dim__dates.id", index=True)
    length_min: Optional[int]
    genre: Optional[list[Genre]] = Field(sa_column=Column(JSON))
    directors: Optional[list[FullName]] = Field(sa_column=Column(JSON))
    writers: Optional[list[FullName]] = Field(sa_column=Column(JSON))
    actors: Optional[list[FullName]] = Field(sa_column=Column(JSON))
    plot: Optional[Description]
    languages: Optional[list[Language]] = Field(sa_column=Column(JSON))
    countries: Optional[list[Country]] = Field(sa_column=Column(JSON))
    awards: Optional[Description]
    poster_url: Optional[str] = Field(sa_column=Column(String))
    imdb_votes_number: Optional[int] = Field(nullable=True)
    imdb_id: IMDbId = Field(nullable=False, index=True, unique=True)
    type: MovieType
    dvd_release_date_id: Optional[IdInt] = Field(nullable=True, foreign_key="dwh_dim__dates.id", index=True)
    boxoffice: Optional[DollarsFull]
    production: Optional[list[Company]] = Field(sa_column=Column(JSON))

