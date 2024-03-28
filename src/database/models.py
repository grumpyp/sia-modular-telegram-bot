from src.database.base import Base
from sqlalchemy import Column, Integer, String



class ExampleModel(Base):
    __tablename__ = 'examples'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)