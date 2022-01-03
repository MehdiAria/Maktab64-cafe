from core.db_manager import DBModel, DBManager
from datetime import datetime, timedelta


class Cashier(DBModel):
    TABLE = "cashier"
    aliases = {"_id": "id"}

    def __init__(self, name, last_name, email, phone, password, _id=None) -> None:
        self.alias_for("_id", "id")
        self.name = name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.password = password
        if _id:
            self._id = _id


class CafeTable(DBModel):
    TABLE = "cafe_table"

    def __init__(self, number, space, id) -> None:
        self.number = number
        self.space = space
        self.id = id


class MenuItems(DBModel):
    TABLE = 'menu_items'
    aliases = {"_id": "id"}

    def __init__(self, category_id, discount, name, price, image_url, serving_time, _id=None) -> None:
        self.category_id = category_id
        self.name = name
        self.discount = discount
        self.price = price
        self.image_url = image_url
        self.serving_time = serving_time
        if _id:
            self.id = _id

    @classmethod
    def read_with_category(cls):
        db = DBManager()
        menu_items = db.read_all(cls)
        categories = db.read_all(Category)
        items_category_dict = {}
        items_category_dict = db.query("SELECT menu_items.name, menu_items.img_url, menu_items.price,"
                                       "categories.name FROM menu_items INNER JOIN categories ON menu_items.id = categories.id",
                                       fetch="all")
        print(items_category_dict)
        # for i in categories:
        #     i: Category
        #     items_category_dict[i.name] = []
        # for item in menu_items:
        #     item: cls
        #     category_id = item.category_id
        #     category: Category
        #     category_name = category.name
        #     items_category_dict[category_name].append(item)

        # for item in menu_items:
        #     pass


class Status(DBModel):
    TABLE = "status"

    def __init__(self, name, description, id=None):
        self.name = name
        self.description = description
        if id: self.id = id


class Category(DBModel):
    TABLE = "categories"
    aliases = {"_id": "id"}

    def __init__(self, name, category_id=None, _id=0):
        self.name = name
        self.category_id = category_id
        self._id = _id

    @classmethod
    def category_item(cls):
        db = DBManager()
        categories = db.read_all(Category)
        items = db.read_all(MenuItems)
        items_id = [i.category_id for i in items]
        c_items_dict = {}
        for c in categories:
            c: Category
            if not c.category_id:  # selecting just base categories
                items_list = []
                for i in items:
                    i: MenuItems
                    if i.category_id == c._id:
                        items_list.append(i)
                if items_list:  # it means that some items have this category_id
                    c_items_dict[c.name] = items_list  # "category": [...]
                else:  # in this case -> "base_category": {"child_category": [...] }
                    for child_c in categories:
                        child_c: Category
                        if child_c.category_id == c._id and (child_c._id in items_id):
                            m_list = []
                            for m in items:
                                z: MenuItems
                                if m.category_id == child_c._id:
                                    m_list.append(m)
                            if c.name in c_items_dict.keys():
                                c_items_dict[c.name][child_c.name] = m_list
                            else:
                                c_items_dict[c.name] = {child_c.name: m_list}
        return c_items_dict


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
# time_t = datetime.now() + timedelta(minutes=10)
# item = MenuItems(1, 0, 'cake', 50000, 'img_url', time_t)
# db = DBManager().create(item)
# cashier = Cashier("cashier", "cashier_id", "example@gmail.com", "0987654321111", "0234832")
# DBManager().create(cashier)
# tbl = CafeTable(1, 3, 1)
# dbt = DBManager().create(tbl)
# stat = Status('error', 'Error from server!', 1)
# dbs = DBManager().create(stat)
# rece = Receipt(5000, 4999, 1)
# dbr = DBManager().create(rece)
# order = Order(0, 10, 1, 1, 1)
# dbr = DBManager().create(order)
# dbdel = DBManager().delete(order)  # for_test
# print(DBManager().query("SELECT * FROM cashier", fetch="all"))
# print(len(DBManager().query("SELECT * FROM cashier", fetch=2)))
# db= DBManager()
# items_category_dict = db.query("SELECT menu_items.name, menu_items.image_url, menu_items.price,"
#                                        "categories.name FROM menu_items INNER JOIN categories ON menu_items.id = categories.id",
#                                        fetch="all")

# items_category_dict = db.query(
#     "Select categories.name as categories_name, menu_items.name from categories inner join menu_items on menu_items.category_id = categories.id",
#     fetch="all")
# for item in items_category_dict:
#     print(dict(item))

print(DBManager().read_filter(CafeTable, "is_empty = true"))