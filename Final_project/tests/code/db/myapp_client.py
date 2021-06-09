from datetime import datetime

import exceptions
import settings
from db.base_client import MysqlClient
from db.models import MyappUserTable


class MyappDBClient(MysqlClient):
    table = MyappUserTable
    tables = [MyappUserTable]

    def __init__(self, db_name=settings.APP_SETTINGS.DB_NAME, **kwargs):
        super().__init__(db_name=db_name, **kwargs)
        self.base_query = self.session_autocommit.query(self.table)
        self.check = self.Check(self)

    def get_all_users(self):
        return self.base_query.all()

    def get_users(self, **kwargs):
        return self.base_query.filter_by(**kwargs).all()

    def get_user(self, **kwargs):
        return self.base_query.filter_by(**kwargs).one_or_none()

    def create_user(self, username: str, password: str, email: str, access: bool = None,
                    active: bool = None, start_active_time: datetime = None):
        obj = self.table(username=username, password=password, email=email,
                         access=access, active=active, start_active_time=start_active_time)
        self.session.add(obj)
        self.session.commit()
        return obj

    def delete_user(self, user_obj):
        self.session.delete(user_obj)
        self.session.commit()

    def delete_users_by_filter(self, **kwargs):
        self.base_query.filter_by(**kwargs).delete()

    def user_exists(self, **kwargs):
        return self.session_autocommit.query(self.base_query.filter_by(**kwargs).exists()).scalar()

    class Check:
        def __init__(self, api):
            self.api = api

        @staticmethod
        def _dict_to_str(dct):
            lst = [f"{k.capitalize()}: {v}" for k, v in dct.items()]
            return f'{". ".join(lst)}'

        def is_user_exists(self, **kwargs):
            if self.api.user_exists(**kwargs):
                return True
            raise exceptions.DBClientCheckingException(f"User does not exists. {self._dict_to_str(kwargs)}")

        def is_not_user_exists(self, **kwargs):
            if not self.api.user_exists(**kwargs):
                return True
            raise exceptions.DBClientCheckingException(f"User exists. {self._dict_to_str(kwargs)}")
