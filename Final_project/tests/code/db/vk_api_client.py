from db.base_client import MysqlClient
import settings
from db.models import VkIdTable


class VkApiDBClient(MysqlClient):
    table = VkIdTable
    tables = [VkIdTable]

    def __init__(self, db_name=settings.MOCK_SETTINGS.DB_NAME, **kwargs):
        super().__init__(db_name=db_name, **kwargs)
        self.base_query = self.session_autocommit.query(self.table)

    def get_vk_id(self, username):
        resp = self.base_query.filter_by(username=username).first()
        if resp:
            return resp.vk_id
        else:
            return None

    def set_vk_id(self, username, vk_id):
        query = self.base_query.filter_by(username=username)
        exists = self.session_autocommit.query(query.exists()).first()[0]
        if exists:
            obj = query.first()
            obj.vk_id = vk_id
            self.session.commit()
        else:
            obj = self.table(username=username, vk_id=vk_id)
            self.session.add(obj)
            self.session.commit()

    def delete_vk_id(self, username):
        self.base_query.filter_by(username=username).delete()
