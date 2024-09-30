# Movie Revenues and IMDb data pipeline prototype
### FM Data Engineer role recruitment task

The main pipeline services and its description are available in `main.ipynb`

### Actions needed to run code 

- Install SQLite version 3.40 or above your machine (not covered in instruction)<br>
- Install Python version 3.12 your machine (not covered in instruction)<br>
- In terminal with project folder as active directory: <br>

<br>
Windows:

```
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
python -m ipykernel install --user --name=.venv
jupyter lab
```
<br>
Linux or Mac:

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 -m ipykernel install --user --name=.venv
jupyter lab
```

### Task description
Most of our personnel in Poland love movies and some of us like to analyze box office performance. Your task is to ingest revenue per day .csv file, enrich it with data from the omdb api, and design a data model (using basic dimensional modeling techniques).

 - Analyze revenues_per_day.csv file and OMDb API examples (OMDb API - The Open Movie Database https://www.omdbapi.com/);
 - Design a simple data model that includes at least one fact table and two dimensions. Create an ER diagram with tables and columns.
 - Register for omdbapi free keyOMDb API - The Open Movie Database https://www.omdbapi.com/apikey.aspx
 - Build an end-to-end pipeline that feeds your data model from revenues_per_day.csv and omdb api. You can use a data warehouse engine of your choice or a notebook with pandas/polaris.
 - Create a ranking dashboard based on your model.
