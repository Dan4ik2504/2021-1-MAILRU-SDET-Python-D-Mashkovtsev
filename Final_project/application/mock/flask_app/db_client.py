import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import VkIdTable, Base
import settings


class MysqlClient:

    def __init__(self, user=settings.DATABASE_SETTINGS.USER, password=settings.DATABASE_SETTINGS.PASSWORD,
                 db_name=settings.MOCK_SETTINGS.DB_NAME,
                 host=settings.DATABASE_SETTINGS.HOST, port=settings.DATABASE_SETTINGS.PORT,
                 autoconnect=True):
        self.user = user
        self.password = password
        self.db_name = db_name

        self.host = host
        self.port = port

        self.engine = None
        self.connection = None
        self.session = None

        if autoconnect:
            self.connect()

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
        self.execute_query(f'USE {self.db_name}', fetch=False)
        self.connection.close()
        self.create_tables()
        self.connect()

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def get_vk_id(self, username):
        resp = self.session.query(VkIdTable).filter_by(username=username).first()
        if resp:
            return resp
        else:
            return None
