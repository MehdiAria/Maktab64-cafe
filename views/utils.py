from core.db_manager import DBManager
from models.model import Cashier

def get_user_by_cookie(request, cashiers):
    cashier_id = request.cookies.get('cashier_logged_in_id', None)
    cashier_token = request.cookies.get('cashier_logged_in_key', None)

    # print(cashier_id, cashier_token)

    if cashier_id == None or cashier_token == None:
        return None
    else:
        db = DBManager()
        cashier = db.read_filter(Cashier, token=cashier_token)
        return cashier
