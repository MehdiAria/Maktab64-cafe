import psycopg2
from psycopg2._psycopg import connection, cursor


class DBManager:
    DEFAULT_HOST = "tyke.db.elephantsql.com"
    DEFAULT_USER = "gcjyvums"
    DEFAULT_PORT = 5432
    DEFAULT_DATABASE = "gcjyvums"
    DEFAULT_PASSWORD = "bcpgqn0RasAF7HlsbsgouCdHJjY7FkxY"

    def __init__(self, password=DEFAULT_PASSWORD, database=DEFAULT_DATABASE, user=DEFAULT_USER, host=DEFAULT_HOST,
                 port=DEFAULT_PORT) -> None:
        self.database = database
        self.password = password
        self.user = user
        self.host = host
        self.port = port

        self.conn: connection = psycopg2.connect(dbname=self.database, user=self.user, host=self.host, port=self.port,
                                                 password=self.password)


db1 = DBManager()
