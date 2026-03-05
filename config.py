"""
Configuration for NCAA pool apps. Prefer environment variables for secrets.
On Python Anywhere: set env vars in the Web app / Tasks configuration.
"""
import os

# Database (ncaa_tourney)
DB_HOST = os.environ.get("NCAA_DB_HOST", "erae22.mysql.pythonanywhere-services.com")
DB_USER = os.environ.get("NCAA_DB_USER", "erae22")
DB_PASSWORD = os.environ.get("NCAA_DB_PASSWORD", "7623chz2g4")
DB_NAME = os.environ.get("NCAA_DB_NAME", "erae22$ncaa_tourney")

def get_mysql_connection_params():
    return {
        "host": DB_HOST,
        "user": DB_USER,
        "password": DB_PASSWORD,
        "database": DB_NAME,
    }

def get_sqlalchemy_uri():
    return "mysql+mysqlconnector://{user}:{password}@{host}/{database}".format(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        database=DB_NAME,
    )

# RapidAPI (basketapi1) for NCAA scores
RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY", "b88fd41b6amsh5775253c68a3727p1f2f1djsn80959b53b4a8")
RAPIDAPI_HOST = os.environ.get("RAPIDAPI_HOST", "basketapi1.p.rapidapi.com")
RAPIDAPI_BASE_URL = os.environ.get(
    "RAPIDAPI_BASE_URL", "https://basketapi1.p.rapidapi.com"
)

def get_rapidapi_headers():
    return {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST,
    }
