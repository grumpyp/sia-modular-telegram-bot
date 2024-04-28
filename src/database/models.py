from src.database.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


# MTM Subscriptions Table
subscriptions_table = Table('subscriptions', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('event_id', Integer, ForeignKey('events.event_id'), primary_key=True),
    Column('subscription_date', DateTime, default=datetime.utcnow)  # Default to current UTC time
)

# Users model derived from telegram api
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    
    events = relationship("Event", secondary=subscriptions_table, back_populates="subscribers")

# Events model
class Event(Base):
    __tablename__ = 'events'
    
    event_id = Column(Integer, primary_key=True)
    event_name = Column(String)
    event_description = Column(String)
    
    subscribers = relationship("User", secondary=subscriptions_table, back_populates="events")
