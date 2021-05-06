from sqlalchemy import Column, Integer, String
from sqlalchemy_utils import URLType
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class NumberOfRequests(Base):
    __tablename__ = 'number_of_requests'

    id = Column(Integer, primary_key=True, autoincrement=True)
    count = Column(Integer, nullable=False)


class NumberOfRequestsByType(Base):
    __tablename__ = 'number_of_requests_by_type'

    id = Column(Integer, primary_key=True, autoincrement=True)
    method = Column(String(10), nullable=False)
    count = Column(Integer, nullable=False)


class MostFrequentRequests(Base):
    __tablename__ = 'most_frequent_requests'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(URLType, nullable=False)
    count = Column(Integer, nullable=False)


class LargestRequests(Base):
    __tablename__ = 'largest_requests'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(URLType, nullable=False)
    status_code = Column(Integer, nullable=False)
    size = Column(Integer, nullable=False)
    ip = Column(String(15), nullable=False)


class UsersByNumberOfRequests(Base):
    __tablename__ = 'users_by_number_of_requests'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String(15), nullable=False)
    count = Column(Integer, nullable=False)
