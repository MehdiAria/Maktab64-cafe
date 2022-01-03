import unittest as ut
from models.model import *
from core.db_manager import DBManager


class TestAlias(ut.TestCase):
    def setUp(self) -> None:
        from random import randint
        self.db = DBManager()
        cashiers = self.db.read_all(Cashier)
        self.cashier_id = cashiers[randint(0, len(cashiers))]._id

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
        self.assertIsInstance(DBManager().read(Cashier, 1), Cashier)

    def test_read_all_filter(self):
        self.assertIsInstance(self.db.read_filter(CafeTable, "is_empty = true"), list)
        self.assertIs(self.db.read_filter(CafeTable, "is empty_true")[0], CafeTable)
        self.assertIs(self.db.read_filter(CafeTable, "is empty_true")[-1], CafeTable)
