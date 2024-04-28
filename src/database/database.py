from sqlalchemy import create_engine
from src.database.base import Base
from src.database.models import *
from config import settings


if settings.DEVELOPMENT:
    DATABASE_URL = "sqlite:///./local_dev_db.db"
else:
    SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# create the tables 
Base.metadata.create_all(engine)