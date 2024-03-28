from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.base import Base
from src.database.models import *
from main import settings


if settings.DEVELOPMENT:
    DATABASE_URL = "sqlite:///./local_dev_db.db"
else:
    SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create the tables 
Base.metadata.create_all(engine)