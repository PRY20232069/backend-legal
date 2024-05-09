import logging
from typing import Iterator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from settings import DB_CONNECTION_URI

# Models
from appV1.models.user import User
from appV1.models.profile import Profile
from appV1.models.bank import Bank
from appV1.models.contract import Contract
from appV1.models.term import Term

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

engine = create_engine(
    DB_CONNECTION_URI,
    future=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)

def get_session() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()