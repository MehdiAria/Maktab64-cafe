from datetime import datetime
from core.db_manager import DBModel, DBManager
from models.exceptions import *
from models.utils import number_check
from core.logger import create_logger

logger = create_logger(__file__, file_skip=0)

db = DBManager()


class Cashier(DBModel):
    TABLE = "cashier"
    aliases = {"_id": "id"}

    def __init__(self, name, last_name, email, phone, password, token=None, _id=None) -> None:
        self.alias_for("_id", "id")
        self.name = name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.password = password
        if token:
            self.token = token
        if _id:
            self._id = _id


class CafeTable(DBModel):
    TABLE = "cafe_table"
    is_empty: bool
    space: int
    id: int
    is_del: bool

    def __init__(self, is_empty, is_del, space,id=None) -> None:
        self.is_empty = is_empty
        self.space = space
        self.is_del = is_del

        if id:
            self.id = id

    @classmethod
    def empty_table(cls):
        return DBManager().read_filter(cls, 'is_empty=true')

    @classmethod
    def is_table_empty(cls, _id):
        return True if DBManager().read_filter(cls, f"id = {_id} AND is_empty = true") else False


class MenuItems(DBModel):
    TABLE = 'menu_items'
    aliases = {"_id": "id"}
    _id: int
    category_id: int
    name: str
    discount: int or float
    price: int or float
    image_url: str
    serving_time: str
    is_del: bool

    def __init__(self, category_id, discount, name, price, image_url, serving_time, is_del=False,_id=None) -> None:
        self.category_id = category_id
        self.name = name
        self.discount = discount
        self.price = price
        self.image_url = image_url
        self.serving_time = serving_time
        self.is_del = is_del
        if _id:
            self.id = _id

    @classmethod
    def read_with_category(cls):
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
    id: int
    item_id: int
    number_item: int
    receipt_id: int
    status_id: int
    table_id: int
    time_stamp: datetime

    def __init__(self, item_id, number_item, receipt_id, status_id, table_id, time_stamp=None, id=None, is_del=False):
        self.time_stamp = time_stamp if time_stamp else datetime.now()
        self.data_check(item_id=item_id, receipt_id=receipt_id, status_id=status_id, time_stamp=self.time_stamp,
                        table_id=table_id, number_item=number_item, order_id=id)
        self.item_id = item_id
        self.number_item = number_item
        self.receipt_id = receipt_id
        self.status_id = status_id
        self.table_id = table_id
        if id:
            self.id = id
        self.is_del = is_del

    @staticmethod
    def data_check(order_id, item_id, receipt_id, status_id, table_id, time_stamp, number_item):
        if not isinstance(time_stamp, datetime):
            error = AddOrderError("time_stamp", time_stamp)
            logger.error(error)
            raise error
        number_check(AddOrderError, item_id=item_id, table_id=table_id,
                     receipt_id=receipt_id, status_id=status_id, number_item=number_item,
                     order_id=order_id if order_id else 0)


class Receipt(DBModel):
    TABLE = "receipt"
    aliases = {"_id": "id"}
    total_price: str
    final_price: str
    _id: None
    time_stamp: datetime
    user_token: str
    is_del: bool

    def __init__(self, total_price, final_price, user_token=None, time_stamp=None, _id=None, is_paid=False,
                 is_del=False) -> None:
        self.total_price = total_price
        self.final_price = final_price
        self.user_token = user_token
        self.is_paid = is_paid
        self.is_del = is_del
        self.time_stamp = time_stamp if time_stamp else datetime.now()
        if _id:
            self._id = _id

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
# import inspect
#
# attributes = inspect.getmembers(Order)
# b = [a for a in attributes if not (a[0].startswith('__') and a[0].endswith('__'))]
# print(vars(Receipt)['__annotations__'])
# print(Order.__class__.__dict__)
# print(DBManager().join_filter(Order, (Receipt,)))
# print(DBManager().query("""SELECT cafe_table.id FROM cafe_table INNER JOIN orders ON
# print(float("AKLS;DJASKDJASLJD"))
#     orders.table_id = cafe_table.id INNER JOIN receipt ON orders.receipt_id = receipt.id WHERE receipt_id = 5;""", fetch="one"))
# print(asd)
# print(__name__, __file__)

# asd = DBManager().read_all(Category)
#
# categories = asd


# def read_cat(category_id, db=DBManager()):
#     db: DBManager
#     category = db.read(Category, category_id)
#     category: Category
#     parent_id = category.category_id
#     if parent_id:
#         yield read_cat(parent_id)
#     yield category.name


# def s_cat():
#     for i in categories:
#         if i.category_id:
#             print

# def all_cat():
#     db = DBManager()
#     cats = db.read_all(Category)
#     cat_list = {}
#     for i in cats:
#         i: Category
#         parent_cat = read_cat(i._id, db)
#         cat_list[i._id] = parent_cat
#         # if parent_cat != i.name:
#         # # print(i.name, "-> ", parent_cat)
#         # pr_ = cat_list.get(parent_cat, None)
#         # # print("\n",pr_)
#         # if pr_ :
#         #     print(cat_list)
#         #     print(pr_, " klasdjalsdj", parent_cat, i.name)
#         #     cat_list[parent_cat] += i.name
#         # else:
#         #     # print(parent_cat)
#         #     print(i.name, parent_cat," asdasd")
#         #     cat_list[parent_cat] = [i.name]
#         # # print(cat_list)
#
#     return cat_list
#
#
# asd = all_cat()
#
# items = DBManager().read_all(MenuItems)
# menu_cat = {}
# for i in items:
#     i: MenuItems
#     a = menu_cat.get(asd[i.category_id], None)
#     if a:
#         menu_cat[asd[i.category_id]].append(i)
#     else:
#         menu_cat[asd[i.category_id]] = [i]
# print(menu_cat)

# n = datetime.now()
# print(all_cat_find())
# m = datetime.now()
# print(m - n)
# def cat_find(c_id):
#     for mn in all_categories:
#         mn: Category
#         if mn._id == c_id:
#             return mn
#
#
# def cat_parent(c):
#     c: Category
#     p_id = c.category_id
#     if p_id:
#         return cat_parent(cat_find(p_id))
#     return c
#
#
# def all_cat_find():
#     cat_dict = {}
#     for c in all_categories:
#         c: Category
#         cat_dict[c._id] = cat_parent(c).name
#     return cat_dict
#
# def menu_set():
#     cat_items ={}
#     cat_dict = all_cat_find()
#     for i in all_items:
#         i:MenuItems
#         alias = cat_dict[i.category_id]
#         if cat_items.get(alias, None):
#             cat_items[alias] .append(i)
#         else:
#             cat_items[alias] = [i]
#     return cat_items

