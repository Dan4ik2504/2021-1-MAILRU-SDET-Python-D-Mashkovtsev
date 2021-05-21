from db.base_client import MysqlClient
import settings
from db.models import VkIdTable


class VkApiDBClient(MysqlClient):
    table = VkIdTable

    def __init__(self, db_name=settings.MOCK_SETTINGS.DB_NAME, **kwargs):
        super().__init__(db_name=db_name, **kwargs)

    def get_vk_id(self, username):
        resp = self.session.query(self.table).filter_by(username=username).first()
        if resp:
            return resp.vk_id
        else:
            return None

    def set_vk_id(self, username, vk_id):
        query = self.session.query(self.table).filter_by(username=username)
        exists = self.session.query(query.exists()).first()[0]
        if exists:
            obj = query.first()
            obj.vk_id = vk_id
        else:
            obj = self.table(username=username, vk_id=vk_id)
            self.session.add(obj)
