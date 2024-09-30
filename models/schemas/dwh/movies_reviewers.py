from sqlmodel import Field
from models.schemas.dwh import DWHSQLModel


class DWHMovieReviewer(DWHSQLModel, table=True):
    __tablename__ = "dwh_dim__movies_reviewers"

    name: str = Field(index=True, unique=True, nullable=False)

