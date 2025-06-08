import os
from dotenv import load_dotenv

# Set base directory of the app
basedir = os.path.abspath(os.path.dirname(__file__))

# Load the .env and .flaskenv variables
load_dotenv(os.path.join(basedir, ".env"))


class Config(object):
    """
    Set the config variables for the Flask app

    """

    SECRET_KEY = os.environ.get("SECRET_KEY") or "secret_key"

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "postgresql+psycopg2://postgres:g&yTSwhHJ5@localhost/ta-db?options=-csearch_path%3Dmembers"
    # or "sqlite:///" + os.path.join(basedir, "app.db")
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_KEY_SECRET = os.environ.get("API_KEY_SECRET") or 'your_master_secret'
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or "secret_jwt_key"
