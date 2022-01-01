from core.db_manager import DBModel, DBManager
from datetime import datetime, timedelta


class Cashier(DBModel):
    TABLE = "cashier"

    def __init__(self, name, last_name, email, phone, password, id=0) -> None:
        self.name = name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.password = password
        self.id = id


class CafeTable(DBModel):
    TABLE = "cafe_table"

    def __init__(self, number, space, id) -> None:
        self.number = number
        self.space = space
        self.id = id


class MenuItems(DBModel):
    TABLE = 'menu_items'

    def __init__(self, category_id, discount, name, price, image_url, serving_time, id=0) -> None:
        self.category_id = category_id
        self.name = name
        self.discount = discount
        self.price = price
        self.image_url = image_url
        self.serving_time = serving_time
        self.id = id


class Status(DBModel):
    TABLE = "status"

    def __init__(self, name, description, id=0):
        self.name = name
        self.description = description
        self.id = id


class Category(DBModel):
    TABLE = "categories"

    def __init__(self, name, category_id=None, id=0):
        self.name = name
        self.category_id = category_id
        self.id = id


class Order(DBModel):
    TABLE = "orders"

    def __init__(self, item_id, number_item, receipt_id, status_id, table_id, id=0):
        self.item_id = item_id
        self.number_item = number_item
        self.receipt_id = receipt_id
        self.status_id = status_id
        self.table_id = table_id
        self.time_stamp = datetime.now()
        self.id = id


class Receipt(DBModel):
    TABLE = "receipt"

    def __init__(self, total_price, final_price, id=0) -> None:

        self.total_price = total_price
        self.final_price = final_price
        self.time_stamp = datetime.now()
        self.id = id


# cat = Category("cake")
# db1 = DBManager().create(cat)
time_t = datetime.now() + timedelta(minutes=10)
item = MenuItems(1, 0, 'cake', 50000, 'img_url', time_t)
db = DBManager().create(item)
