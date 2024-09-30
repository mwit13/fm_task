from sqlmodel import Field
from models.schemas.dwh import DWHSQLModel


class DWHDistributor(DWHSQLModel, table=True):
    __tablename__ = "dwh_dim__distributors"

    name: str = Field(index=True, unique=True, nullable=False)

