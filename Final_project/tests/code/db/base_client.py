import sqlalchemy
from sqlalchemy.orm import sessionmaker

import settings


class MysqlClient:
    session: sqlalchemy.orm.Session = None
    session_autocommit: sqlalchemy.orm.Session = None
    engine: sqlalchemy.engine.Engine = None
    connection: sqlalchemy.engine.Connection = None
    tables = None

    def __init__(self, user=settings.DATABASE_SETTINGS.USER, password=settings.DATABASE_SETTINGS.PASSWORD,
                 db_name=settings.APP_SETTINGS.DB_NAME,
                 host=settings.DATABASE_SETTINGS.HOST, port=settings.DATABASE_SETTINGS.PORT,
                 autoconnect=True, autotruncate_tables=True):
        self.user = user
        self.password = password
        self.db_name = db_name

        self.host = host
        self.port = port

        if autoconnect:
            self.connect()
            if autotruncate_tables:
                self.truncate_tables()

    def connect(self, db_created=True):
        db = self.db_name if db_created else ''

        self.engine = sqlalchemy.create_engine(
            f'{settings.DATABASE_SETTINGS.URL}/{db}',
            encoding='utf8'
        )
        self.connection = self.engine.connect()
        self.session_autocommit = sessionmaker(bind=self.connection.engine,
                                               autocommit=True
                                               )()
        self.session = sessionmaker(bind=self.connection.engine)()

    def execute_query(self, query, fetch=True):
        res = self.connection.execute(query)
        if fetch:
            return res.fetchall()

    def recreate_db(self):
        self.connect()
        self.execute_query(f'DROP database if exists {self.db_name}', fetch=False)
        self.execute_query(f'CREATE database {self.db_name}', fetch=False)
        self.execute_query(f'USE {self.db_name}', fetch=False)
        self.connection.close()

    def truncate_table(self, table):
        self.session.query(table).delete()
        self.session.commit()

    def truncate_tables(self):
        if self.tables:
            for table in self.tables:
                self.truncate_table(table)
