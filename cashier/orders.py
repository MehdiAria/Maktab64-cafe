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
    if request.method == 'GET':
        return render_template('cashier/orders.html', data=data)
    elif request.method == 'POST':
        order = db.read(Order, int(request.form.get('_id')))
        order.is_del = True if request.form.get('is_del') == 'true' else False
        order.item_id = request.form.get('is_del')
        order.status_id = request.form.get('status_id')
        order.number_item = request.form.get('number_item')
        db.update(order)
        return 'Success'




