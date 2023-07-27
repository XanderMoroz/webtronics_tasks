import databases

from app.core.config import settings

DB_USER = settings.DEFAULT_DB_USER
DB_PASS = settings.DEFAULT_DB_PASS
DB_HOST = settings.DEFAULT_DB_HOST
DB_PORT = settings.DEFAULT_DB_PORT
DB_NAME = settings.DEFAULT_DB_NAME
# DB url definition
# DB_NAME = "boiler1"
SQLALCHEMY_DATABASE_URL = (f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

database = databases.Database(SQLALCHEMY_DATABASE_URL)
