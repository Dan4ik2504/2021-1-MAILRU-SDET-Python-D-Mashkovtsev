from sqlalchemy import Column, Integer, String, SmallInteger, DateTime, Text
from sqlalchemy.orm import declarative_base

import settings

Base = declarative_base()


class MyappUserTable(Base):
    __tablename__ = settings.APP_SETTINGS.TABLE_USERS_NAME

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(String(16), unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(64), nullable=False, unique=True)
    access = Column(SmallInteger)
    active = Column(SmallInteger)
    start_active_time = Column(DateTime, default=None)


class VkIdTable(Base):
    __tablename__ = settings.MOCK_SETTINGS.TABLE_VK_ID_NAME

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(16), nullable=False)
    vk_id = Column(Text)
