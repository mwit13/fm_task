from sqlmodel import Field

from models.definitions.objects import DateValue
from models.schemas.dwh import DWHSQLModel


class DWHDate(DWHSQLModel, table=True):
    __tablename__ = "dwh_dim__dates"

    value: DateValue = Field(index=True, unique=True, nullable=False)
