from models.schemas.dwh.dates import DWHDate
from models.schemas.dwh.fact_revenue import DWHDayRevenue
from models.schemas.dwh.movies import DWHMovie
from models.schemas.dwh.distributors import DWHDistributor
from models.schemas.dwh.movies_reviewers import DWHMovieReviewer
from models.schemas.dwh.reviews_results import DWHReviewResult
from models.schemas.stg.revenue_per_day import STGDayRevenue
from models.schemas.stg.movies_details import STGMovie

stg_orms = [STGDayRevenue, STGMovie,]
dwh_orms = [DWHMovieReviewer, DWHMovie, DWHReviewResult, DWHDistributor, DWHDate, DWHDayRevenue,]

