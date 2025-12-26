from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from server.decorators.singleton import singleton

Base = declarative_base()


@singleton
class DBManager:

    def __init__(self, db_name=None):
        print(db_name)
        self.engine = create_engine(f'sqlite:///{db_name}.db', connect_args={'check_same_thread': False})
        self.Session = scoped_session(sessionmaker(bind=self.engine))

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def get_session(self):
        return self.Session()

    def __enter__(self):
        self.current_session = self.Session()
        return self.current_session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.current_session.rollback()
        else:
            self.current_session.commit()
        self.Session.remove()
