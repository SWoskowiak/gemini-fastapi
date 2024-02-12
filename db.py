"""The db module. A simple singleton database class."""
# pylint: disable=line-too-long

import os
from contextlib import contextmanager
from sqlalchemy import create_engine, MetaData, delete
from sqlalchemy.orm import sessionmaker

class DB:
    """Our simple singleton database class. Used to create a single database connection and session for the app."""
    _instance = None

    def __new__(cls):
        """Make this DB class a singleton."""
        if cls._instance is None:
            cls._instance = super(DB, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Define the database engine and session."""
        self._engine = None
        self._session = None

    @property
    def engine(self):
        """Create a database engine if it doesn't exist yet."""
        if self._engine is None:
            db_url: str = os.getenv('DB_URL')
            if db_url is None:
                raise ValueError('Missing environment variable: DB_URL. Set it to a valid sqlalchemy compatible database URL.')
            self._engine = create_engine(db_url, future=True)
        return self._engine

    @property
    def session(self):
        """Create a session to interact with the database."""
        if self._session is None:
            _ = self.engine  # This will create the engine if it doesn't exist yet
            self._session = sessionmaker(bind=self._engine)
        return self._session

    @contextmanager
    def get_session(self):
        """Provide a transactional scope around a session."""
        session = self.session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def truncate_all(self):
        """Truncate all tables in the database."""
        env = os.getenv('ENV')
        # Whitelist the environments that can truncate all tables
        if env not in ['local', 'test']:
            raise EnvironmentError('Cannot truncate all tables outside of a local/test environment')

        with self.get_session() as session:
            meta = MetaData()
            meta.reflect(bind=self._engine)

            for table in reversed(meta.sorted_tables):
                session.execute(delete(table))

            session.commit()

db = DB()
