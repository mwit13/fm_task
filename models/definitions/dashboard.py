from ipywidgets.widgets import Dropdown
from pipeline.dashboard.successful import MostSuccessfulPlotDetails

most_successful_plots_definitions = dict(
    per_month=MostSuccessfulPlotDetails(
        query="SELECT * FROM per_month_revenues",
        x='release_month',
        y='total_revenue',
        labels={'release_month': 'Release Month', 'total_revenue': 'Average Revenue'},
        title='Most fruitful months',
        text='total_revenue'
    ),
    genres=MostSuccessfulPlotDetails(
        query="SELECT * FROM genre_revenues LIMIT 30",
        x='genre',
        y='total_revenue',
        labels={'genre': 'Genre', 'total_revenue': 'Total Revenue'},
        title='Most fruitful genres',
        text='total_revenue'
    ),
    actors=MostSuccessfulPlotDetails(
        query="SELECT * FROM actors_revenues LIMIT 30",
        x='actor',
        y='total_revenue',
        labels={'actor': 'Actor', 'total_revenue': 'Total Revenue'},
        title='Most successful actors',
        text='total_revenue'
    ),
    countries=MostSuccessfulPlotDetails(
        query="SELECT * FROM country_revenue LIMIT 30",
        x='country',
        y='total_revenue',
        labels={'country': 'Country', 'total_revenue': 'Total Revenue'},
        title='Most successful countries',
        text='total_revenue'
    ),
    directors=MostSuccessfulPlotDetails(
        query="SELECT * FROM directors_revenues LIMIT 30",
        x='director',
        y='total_revenue',
        labels={'director': 'Director', 'total_revenue': 'Total Revenue'},
        title='Most successful directors',
        text='total_revenue'
    ),
    movies=MostSuccessfulPlotDetails(
        query="SELECT * FROM movies_revenues LIMIT 30",
        x='title',
        y='total_revenue',
        labels={'title': 'Movie title', 'total_revenue': 'Total Revenue'},
        title='Most fruitful movies',
        text='total_revenue'
    ),
    rating=MostSuccessfulPlotDetails(
        query="SELECT * FROM per_rating_revenues",
        x='rating',
        y='total_revenue',
        labels={'rating': 'Age rating type', 'total_revenue': 'Total Revenue'},
        title='Most fruitful age ratings',
        text='total_revenue'
    ),
    per_year=MostSuccessfulPlotDetails(
        query="SELECT * FROM per_year_revenues",
        x='release_year',
        y='total_revenue',
        labels={'release_year': 'Release year', 'total_revenue': 'Average Revenue'},
        title='Most fruitful years',
        text='total_revenue'
    ),
    writers=MostSuccessfulPlotDetails(
        query="SELECT * FROM writers_revenues LIMIT 30",
        x='writer',
        y='total_revenue',
        labels={'writer': 'Writer', 'total_revenue': 'Total Revenue'},
        title='Most successful writers',
        text='total_revenue'
    ),
)

dropdown = Dropdown(
    options=[
        ('Month', 'per_month'),
        ('Genres', 'genres'),
        ('Actors', 'actors'),
        ('Countries', 'countries'),
        ('Directors', 'directors'),
        ('Titles', 'movies'),
        ('Age Rating', 'rating'),
        ('Year', 'per_year'),
        ('Writers', 'writers'),
    ],
    value="genres",  # Default view
    description='Select',
)
