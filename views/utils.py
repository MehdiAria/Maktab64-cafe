from core.db_manager import DBManager
from models.model import Cashier, Receipt
import uuid, os


def get_cashier_by_cookie(request):
    cashier_id = request.cookies.get('cashier_logged_in_id', None)
    cashier_token = request.cookies.get('cashier_logged_in_token', None)

    if cashier_id == None or cashier_token == None:
        return None
    else:
        db = DBManager()
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
