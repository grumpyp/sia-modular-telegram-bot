from sqlalchemy import create_engine
from src.database.base import Base
from src.database.models import *
from config import settings
from sqlalchemy.orm import sessionmaker


if settings.DEVELOPMENT:
    DATABASE_URL = "sqlite:///./local_dev_db.db"
else:
    SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# create the tables 
Base.metadata.create_all(engine)

# create default events
initial_events = [
    {'event_id': 0, 'event_name': 'alerts', 'event_description': 'info'},
    {'event_id': 1, 'event_name': 'alerts', 'event_description': 'warning'},
    {'event_id': 2, 'event_name': 'alerts', 'event_description': 'error'},
    {'event_id': 3, 'event_name': 'alerts', 'event_description': 'critical'},
    {'event_id': 4, 'event_name': 'balance', 'event_description': 'balance treshhold'},
    {'event_id': 5, 'event_name': 'storage', 'event_description': 'storage treshhold'}
]

Session = sessionmaker(bind=engine)
session = Session()

# Insert initial events if not present
for event_data in initial_events:
    event_exists = session.query(Event).filter_by(event_id=event_data['event_id']).first()
    if not event_exists:
        new_event = Event(**event_data)
        session.add(new_event)

# Commit the session to save changes
session.commit()