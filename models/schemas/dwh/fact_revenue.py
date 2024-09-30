from typing import Optional

from sqlalchemy import UniqueConstraint
from sqlmodel import Field

from models.definitions.objects import IdInt, DollarsFull
from models.schemas.dwh import DWHSQLModel


class DWHDayRevenue(DWHSQLModel, table=True):
    __tablename__ = "dwh_fact__revenues"

    movie_id: IdInt = Field(nullable=False, foreign_key="dwh_dim__movies.id", index=True)
    distributor_id: Optional[IdInt] = Field(nullable=True, foreign_key="dwh_dim__distributors.id", index=True)
    date_id: IdInt = Field(nullable=False, foreign_key="dwh_dim__dates.id", index=True)
    revenue: DollarsFull = Field(nullable=False)
    theaters_number: Optional[int] = Field(nullable=True)

    __table_args__ = (UniqueConstraint('movie_id', 'date_id', name='uix_movie_id_date_id'),)
