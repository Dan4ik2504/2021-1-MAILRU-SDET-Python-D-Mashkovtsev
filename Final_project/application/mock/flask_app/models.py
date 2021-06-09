from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

import settings

Base = declarative_base()


class VkIdTable(Base):
    __tablename__ = settings.MOCK_SETTINGS.TABLE_VK_ID_NAME

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(length=16))
    vk_id = Column(Text)
