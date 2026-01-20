from server.db.db_manager import DBManager
from server.db.models import User
from server.utils import model_to_dict

class UserService:
    def __init__(self):
        self.db: DBManager = DBManager()

    def get_users(self):
        with self.db as session:
            db_users = session.query(User).all()
            users = [model_to_dict(u) for u in db_users]
            return users

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

