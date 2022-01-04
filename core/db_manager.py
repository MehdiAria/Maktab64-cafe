import psycopg2
from psycopg2._psycopg import connection, cursor
from psycopg2 import extras
from abc import ABC
from core.utils import alias_for_model


class DBModel(ABC):  # abstract base Database model
    TABLE: str  # table name
    PK: str = "id"  # primary key column of the table
    aliases = {}

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} {vars(self)}>"

    @classmethod
    def alias_for(cls, attr, alias):
        cls.aliases[attr] = alias

    def with_alias_dict(self):
        base_dict = vars(self)
        for i in self.aliases.keys():
            if i in base_dict.keys():
                value = base_dict[i]
                base_dict.pop(i)
                base_dict[self.aliases[i]] = value
        return base_dict


class DBManager:
    DEFAULT_HOST = "194.39.205.167"
    DEFAULT_USER = "maktab"
    DEFAULT_PORT = 5432
    DEFAULT_DATABASE = "maktab"
    DEFAULT_PASSWORD = "maktab"

    def __init__(self, password=DEFAULT_PASSWORD, database=DEFAULT_DATABASE, user=DEFAULT_USER, host=DEFAULT_HOST,
                 port=DEFAULT_PORT) -> None:
        self.database = database
        self.password = password
        self.user = user
        self.host = host
        self.port = port
        self.conn: connection = psycopg2.connect(dbname=self.database, user=self.user, host=self.host, port=self.port,
                                                 password=self.password)

    def __del__(self):
        self.conn.close()  # Close the connection on delete

    def __get_cursor(self) -> cursor:
        # Changing the fetch output from Tuple to Dict utilizing RealDictCursor cursor factory
        return self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def create(self, model_instance: DBModel) -> int:
        with self.conn:
            assert isinstance(model_instance, DBModel)
            curs = self.__get_cursor()
            model_vars = model_instance.with_alias_dict()
            model_fields_str = ",".join(
                model_vars.keys())
            model_values_str = ",".join(["%s"] * len(model_vars))
            model_values_tuple = tuple(model_vars.values())
            with curs:
                curs.execute(
                    f"""INSERT INTO {model_instance.TABLE}({model_fields_str}) VALUES ({model_values_str}) RETURNING ID;""",
                    model_values_tuple)
                id = int(curs.fetchone()['id'])
                setattr(model_instance, '_id', id)
                return id

    def read(self, model_class: type, pk):
        assert issubclass(model_class, DBModel)
        with self.conn:
            with self.__get_cursor() as curs:
                curs.execute(f"""SELECT * FROM {model_class.TABLE} WHERE {model_class.PK} = {pk}""")
                res = curs.fetchone()
                reverse_alias = {value: key for key, value in model_class.aliases.items()}
                res = alias_for_model(res, reverse_alias)
                return model_class(**dict(res))

    def update(self, model_instance: DBModel) -> None:
        assert isinstance(model_instance, DBModel)
        with self.conn:
            curs = self.__get_cursor()
            with curs:
                model_vars = vars(model_instance)
                model_pk_value = getattr(model_instance, model_instance.PK)  # value of pk (for ex. 'id' in patient)
                model_set_values = [f"{field} = %s" for field in model_vars]  # -> ['first_name=%s', 'last_name'=%s,...]
                model_values_tuple = tuple(model_vars.values())
                curs.execute(f"""UPDATE {model_instance.TABLE} SET {','.join(model_set_values)}
                    WHERE {model_instance.PK} = {model_pk_value};""", model_values_tuple)

    def delete(self, model_instance: DBModel) -> None:
        assert isinstance(model_instance, DBModel)
        with self.conn:
            curs = self.__get_cursor()
            with curs:
                model_pk_value = getattr(model_instance, model_instance.PK)
                curs.execute(f"""DELETE FROM {model_instance.TABLE} WHERE {model_instance.PK} = {model_pk_value};""")
                delattr(model_instance, 'id')  # deleting attribute 'id' from the deleted instance

    def read_all(self, model_class: type):  # get
        assert issubclass(model_class, DBModel)
        with self.conn:
            curs = self.__get_cursor()
            res = []
            with curs:
                curs.execute(f"""SELECT * FROM  {model_class.TABLE};""")
                models_dict = curs.fetchall()
                for i in models_dict:
                    reverse_alias = {value: key for key, value in model_class.aliases.items()}
                    i = alias_for_model(i, reverse_alias)
                    res.append(model_class(**dict(i)))
            return res  # returns an instance of the Model with inserted values

    def query(self, query: str, fetch: any = None):
        with self.conn:
            curs = self.__get_cursor()
            with curs:
                curs.execute(query)
                if fetch == "one":
                    models_dict = curs.fetchone()
                    return models_dict
                if type(fetch) == int:
                    models_dict = curs.fetchmany(fetch)
                    return models_dict
                elif fetch == 'all':
                    models_dict = curs.fetchall()
                    return models_dict

    def read_filter(self, model_class: type, condition):
        assert issubclass(model_class, DBModel)
        model_dict = self.query(f"SELECT * FROM {model_class.TABLE} WHERE {condition}", fetch='all')
        res = []
        for i in model_dict:
            res.append(model_class(**dict(i)))
        return res

    def read_filter_nowhere(self, model_class: type, condition):
        assert issubclass(model_class, DBModel)
        model_dict = self.query(f"{condition}", fetch='all')
        res = []
        for i in model_dict:
            res.append(model_class(**dict(i)))
        return res


db1 = DBManager()
