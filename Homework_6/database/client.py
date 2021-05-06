import sqlalchemy
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker

from database.models import Base
import settings
from log_analyzer import log_analyzer_settings


class MysqlClient:

    def __init__(self, user=settings.DB.USER, password=settings.DB.PASSWORD, db_name=settings.DB.DB_NAME):
        self.user = user
        self.password = password
        self.db_name = db_name

        self.host = settings.DB.HOST
        self.port = settings.DB.PORT

        self.engine = None
        self.connection = None
        self.session = None

    def connect(self, db_created=True):
        db = self.db_name if db_created else ''

        self.engine = sqlalchemy.create_engine(
            f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{db}',
            encoding='utf8'
        )
        self.connection = self.engine.connect()
        self.session = sessionmaker(bind=self.connection.engine,
                                    autocommit=True,
                                    )()

    def execute_query(self, query, fetch=True):
        res = self.connection.execute(query)
        if fetch:
            return res.fetchall()

    def recreate_db(self):
        self.connect(db_created=False)
        self.execute_query(f'DROP database if exists {self.db_name}', fetch=False)
        self.execute_query(f'CREATE database {self.db_name}', fetch=False)
        self.connection.close()

    def create_table(self, table_name: str):
        if not inspect(self.engine).has_table(table_name):
            Base.metadata.tables[table_name].create(self.engine)

    def create_tables_for_log_analyzer(self):
        for table_name in log_analyzer_settings.TABLE_NAMES:
            self.create_table(table_name)
