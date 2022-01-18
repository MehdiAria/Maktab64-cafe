from model import Cashier
from core.db_manager import DBManager, DBModel

db = DBManager()


if __name__ == '__main__':
    fname = input("Enter Cashier Name: ")
    lname = input("Enter Cashier Last Name: ")
    email = input("Enter Cashier Email: ")
    phone = input("Enter Cashier Phone No.: ")
    pw = input("Enter Cashier Password: ")
    cashier:DBModel = Cashier(fname, lname, email, phone, pw)
    db.create(cashier)