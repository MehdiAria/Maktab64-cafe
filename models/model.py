from core.db_manager import DBModel


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
