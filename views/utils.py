from core.db_manager import DBManager
from models.model import Cashier, Receipt, CafeTable, Order
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
    # del db
    return new_token


def check_table_id(receipt_id, table_id):
    receipt_table = db.all_query(CafeTable,
                                 f"""SELECT cafe_table.id, cafe_table.is_empty, cafe_table.space, cafe_table.is_del
                                                FROM cafe_table INNER JOIN orders ON orders.table_id = cafe_table.id
                                                INNER join receipt ON receipt.id = orders.receipt_id
                                                WHERE receipt.id = {receipt_id} """, fetch="one")
    #  TODO logger here
    receipt_table: CafeTable
    assert int(table_id) == receipt_table.id


def order_operation(request, operator):
    order_id = int(request.form.get('order_id'))
    receipt_id = int(request.cookies.get("receipt_id"))
    table_order: Order
    receipt: Receipt
    receipt = db.read_filter(Receipt, f"id = {receipt_id} AND is_del = false", fetch="one")
    table_order = db.read(Order, order_id)
    item_price = db.query(f"SELECT price FROM menu_items WHERE id = {table_order.item_id}", fetch="one")["price"]
    receipt.total_price += item_price if operator == "+" else -item_price
    receipt.final_price += item_price if operator == "+" else -item_price
    table_order.number_item = table_order.number_item + 1 if operator == "+" else table_order.number_item - 1
    db.update(receipt)
    db.update(table_order)
    return {'number_item': table_order.number_item, "order_id": table_order.id,
            "total_price": receipt.total_price, "final_price": receipt.final_price}
