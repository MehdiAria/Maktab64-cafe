from core.db_manager import DBManager
from models.model import Cashier, Receipt, CafeTable
import uuid, os

db = DBManager()


def get_cashier_by_cookie(request):
    cashier_id = request.cookies.get('cashier_logged_in_id', None)
    cashier_token = request.cookies.get('cashier_logged_in_token', None)

    if cashier_id == None or cashier_token == None:
        return None
    else:
        cashier = db.read_filter(Cashier, f'token=\'{cashier_token}\'')
        return cashier


def set_user_token(receipt):
    db = DBManager()
    receipt: Receipt
    new_token = str(uuid.UUID(bytes=os.urandom(16)))
    receipt.user_token = new_token
    db.update(receipt)
    del db
    return new_token


def check_table_id(receipt_id, table_id):
    receipt_table = db.all_query(CafeTable, f"""SELECT cafe_table.id, cafe_table.is_empty, cafe_table.space
                                                FROM receipt INNER JOIN orders ON orders.receipt_id = receipt.id
                                                INNER join cafe_table ON cafe_table.id = orders.table_id
                                                WHERE receipt.id = {receipt_id} """, fetch="one")
    receipt_table: CafeTable
    assert table_id == receipt_table.id
