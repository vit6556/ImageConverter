from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from common.config.database import POSTGRES_URL


def get_database_engine():
    return create_engine(url=POSTGRES_URL)

class DatabaseSessionManager:
    def __init__(self):
        engine = get_database_engine()
        DatabaseSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        self.session = DatabaseSession()

    def __enter__(self) -> Session:
        return self.session

    def __exit__(self, *args):
        self.session.close()