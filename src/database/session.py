from .database import engine
from sqlalchemy.orm import sessionmaker, Session


sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session(s: Session = sessionlocal) -> Session:
    session = s()
    try:
        yield session
    finally:
        session.close()