from pipeline.ingestion import CSVIngesterDefinition, OMDBAPIFetchDefinition
from models.schemas.stg.revenue_per_day import STGDayRevenue

revenues_per_day_definition = \
    CSVIngesterDefinition(
        filepath='./data_to_ingest/revenues_per_day.csv',
        orm_class=STGDayRevenue,
        separator=',',
        is_header=True
    )

movies_details_api_fetch_definition = \
    OMDBAPIFetchDefinition(
        omdb_address='http://www.omdbapi.com',
        allowed_failed_attempts=10,
        dry_run=False)
