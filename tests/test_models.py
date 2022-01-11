import unittest as ut
from models.model import *
from core.db_manager import DBManager
from models.exceptions import *


class TestAlias(ut.TestCase):
    def setUp(self) -> None:
        from random import randint
        self.db = DBManager()
        cashiers = self.db.read_all(Cashier)
        self.cashier_id = cashiers[randint(0, len(cashiers) - 1)]._id

    def test_alias_cashier(self):
        pass
        # db = DBManager()
        # cashier = Cashier("cashier", "cashier_id", "example@gmail.com", "0987654321111", "0234832")
        # db.create(cashier)
        # cashier_id = cashier.id_getter()
        # read_cashier = db.read(Cashier, cashier_id)
        # self.assertIsInstance(read_cashier, Cashier)
        # read_cashier.name = "asd"
        # db.update(read_cashier)
        # db.delete(cashier)
        # self.assertNotIn("_Cashier__id", Cashier("cashier", "cashier_id", "example@gmail.com", "0987654321111",
        #                                          "0234832", 1).with_alias_dict().keys())

    def test_read_data(self):
        self.assertIsInstance(DBManager().read(Cashier, self.cashier_id), Cashier)

    def test_read_all_filter(self):
        self.assertIsInstance(self.db.read_filter(CafeTable, "is_empty = true"), list)
        self.assertIsInstance(self.db.read_filter(CafeTable, "is_empty = true")[0], CafeTable)
        self.assertIsInstance(self.db.read_filter(CafeTable, "is_empty = true")[-1], CafeTable)

    def test_class_alias(self):
        self.assertIsInstance(Receipt.class_aliases(), list)


class TestValidators(ut.TestCase):
    def test_order_validator(self):
        """item_id, number_item, receipt_id, status_id, table_id, time_stamp=None, id=None"""
        self.assertRaises(AddOrderError, Order, "ten", 1, 17, 1, 1, datetime.now(), 1)
        self.assertRaises(AddOrderError, Order, 19, "asd", 16, 1, 1, datetime.now(), 1)
        self.assertRaises(AddOrderError, Order, 1, 1, "asd", 1, 1, datetime.now(), 1)
        self.assertRaises(AddOrderError, Order, 15, 1, 1, 1, "a", datetime.now(), 1)
        self.assertRaises(AddOrderError, Order, 1, 1, 15, 1, 1, "2020", 1)
        self.assertRaises(AddOrderError, Order, 5, 1, 1, 2, 4, datetime.now(), "123--")



