from core.db_manager import DBModel


class Cashier(DBModel):
    def __init__(self, id, name, last_name, email, phone, password) -> None:
        self.id = id
        self.name = name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.password = password


class Category(DBModel):
    _id: int
    name: str
    category_id: int

    def __init__(self, id, name, category_id=None):
        self._id = id
        self.name = name
        self.category_id = category_id
