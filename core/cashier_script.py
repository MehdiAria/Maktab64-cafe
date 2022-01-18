from models.model import Cashier
from db_manager import DBModel

db = DBModel()


if __name__ == '__main__':
    fname = input("Enter Cashier Name: ")
    lname = input("Enter Cashier Last Name: ")
    email = input("Enter Cashier Email: ")
    phone = input("Enter Cashier Phone No.: ")
    pw = input("Enter Cashier Password: ")
    # cashier = Cashier(fname, lname, email, phone, pw)
