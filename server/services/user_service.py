from server.db.db_manager import DBManager
from server.db.models import User


class UserService:
    def __init__(self):
        self.db: DBManager = DBManager()

    def get_users(self):
        with self.db as session:
            return session.query(User).all()

    def get_user_by_username(self, username):
        with self.db as session:
            user = session.query(User).filter_by(username=username).first()
            session.refresh(user)
            session.expunge(user)
            return user

    def create_user(self, username):
        with self.db as session:
            user = session.query(User).filter_by(username=username).first()
            if user:
                raise Exception(f"User with name: {username} already exists")
            user = User(username=username)
            session.add(user)
            session.flush()
            return user.id

