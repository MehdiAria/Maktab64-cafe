from flask import render_template, request
from core.db_manager import DBManager
from models.model import Order

db = DBManager()


def orders():
    order_list = db.all_query(Order,
                              f"""SELECT * FROM orders WHERE True;""")
    datetime_list = list(
        map(lambda x: 'T'.join(x.time_stamp.__str__().split()), order_list))
    data = zip(order_list, datetime_list)
    # data = {'order_list': order_list, 'datetime_list': datetime_list}
    if request.method == 'GET':
        return render_template('cashier/orders.html', data=data)
    elif request.method == 'POST':
        return 'Success'


def del_order():
    if request.method == 'POST':
        x = request.form.get('order_id')
        obj_order = db.read(Order, x)
        db.delete(obj_order)
        return "order deleted"


def dec_order():
    if request.method == 'POST':
        x = request.form.get('order_id')
        obj_order = db.read(Order, x)

