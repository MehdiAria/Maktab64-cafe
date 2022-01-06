from core.db_manager import DBManager
from models.model import Cashier


def get_cashier_by_cookie(request):
    cashier_id = request.cookies.get('cashier_logged_in_id', None)
    cashier_token = request.cookies.get('cashier_logged_in_token', None)

    if cashier_id == None or cashier_token == None:
        return None
    else:
        db = DBManager()
        cashier = db.read_filter(Cashier, f'token=\'{cashier_token}\'')
        return cashier
