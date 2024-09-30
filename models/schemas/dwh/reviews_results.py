from sqlalchemy import UniqueConstraint
from sqlmodel import Field

from models.definitions.objects import Score, IdInt
from models.schemas.dwh import DWHSQLModel


class DWHReviewResult(DWHSQLModel, table=True):
    __tablename__ = "dwh_dim__reviews_results"

    movie_id: IdInt = Field(nullable=False, foreign_key="dwh_dim__movies.id", index=True)
    reviewer_id: IdInt = Field(nullable=False, foreign_key="dwh_dim__movies_reviewers.id", index=True)
    score_percent: Score = Field(nullable=False)

    __table_args__ = (UniqueConstraint('movie_id', 'reviewer_id', name='uix_movie_id_reviewer_id'),)

