from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class VkIdTable(Base):
    __tablename__ = 'vk_id_table'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(length=16), nullable=False)
    vk_id = Column(Integer, nullable=False)
