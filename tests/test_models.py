import unittest as ut
from models.model import *
from core.db_manager import DBManager


class TestAlias(ut.TestCase):
    def test_alias_cashier(self):
        self.assertNotIn("_Cashier__id", Cashier("cashier", "cashier_id", "example@gmail.com", "0987654321111",
                                                 "0234832", 1).with_alias_dict().keys())


class TestDBManager(ut.TestCase):
    def test_read_data(self):
        self.assertIsInstance(DBManager().read(Cashier, 1), Cashier)
