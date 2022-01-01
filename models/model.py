from core.db_manager import DBModel
from datetime import datetime

class Cashier(DBModel):
    def __init__(self, id, name, last_name, email, phone, password) -> None:
        self.id = id
        self.name = name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.password = password


class Cafe_table(DBModel):
    def __init__(self, id, number, space) -> None:
        self.id = id
        self.number = number
        self.space = space


class menu_items(DBModel):

    def __init__(self,id, discount, name, price, img_url, serving_time) -> None:
        self.id = id
        self.name = name
        self.discount = discount
        self.price = price
        self.img_url = img_url
        self.serving_time = serving_time




class Order(DBModel):
    def __init__(self,id, item_id, number_items, receipt_id, status_id, table_id):
        self.id = id
        self.item_id = item_id
        self.number_items = number_items
        self.receipt_id = receipt_id
        self.status_id = status_id
        self.table_id = table_id
        self.time_stamp = datetime.now()