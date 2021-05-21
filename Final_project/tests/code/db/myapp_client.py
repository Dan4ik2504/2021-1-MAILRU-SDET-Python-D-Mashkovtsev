from datetime import datetime

from db.base_client import MysqlClient
import settings
from db.models import MyappUserTable


class MyappDBClient(MysqlClient):
    table = MyappUserTable

    def __init__(self, db_name=settings.APP_SETTINGS.DB_NAME, **kwargs):
        super().__init__(db_name=db_name, **kwargs)

    def get_all_users(self):
        return self.session.query(self.table).all()

    def get_users(self, **kwargs):
        return self.session.query(self.table).filter_by(**kwargs).all()

    def get_user(self, **kwargs):
        return self.session.query(self.table).filter_by(**kwargs).one_or_none()

    def create_user(self, username: str, password: str, email: str, access: bool=None,
                    active: bool=None, start_active_time: datetime=None):
        obj = self.table(username=username, password=password, email=email,
                         access=access, active=active, start_active_time=start_active_time)
        self.session.add(obj)
