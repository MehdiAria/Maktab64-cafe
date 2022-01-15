from flask import render_template, request
from core.db_manager import DBManager
from models.model import Order, Status

db = DBManager()


def orders():
    order_list = db.query(
        f"SELECT {Order.class_aliases(to_str=True)},menu_items.name as item_name,status.name as status_name FROM orders INNER JOIN status ON orders.status_id=status.id INNER JOIN menu_items ON menu_items.id=orders.item_id;",
        fetch='all')
    print(order_list)
    status_list = db.all_query(Status,
                               f"SELECT * FROM status where True;")
    # order_list = db.query(
    #     f"""-- SELECT * FROM orders INNER JOIN status ON orders.status_id=status.id INNER JOIN menu_items ON menu_items.id=orders.item_id;""")
    # datetime_list = list(
    #     map(lambda x: 'T'.join(x.time_stamp.__str__().split()), order_list))
    # data = zip(order_list, datetime_list)
    if request.method == 'GET':
        return render_template('cashier/orders.html', status=status_list, data=order_list)
    elif request.method == 'POST':
        order = db.read(Order, int(request.form.get('_id')))
        order.is_del = True if request.form.get('is_del') == 'true' else False
        order.item_id = request.form.get('item_id')
        order.status_id = request.form.get('status_id')
        order.number_item = request.form.get('number_item')
        db.update(order)
        return "Edit was successful!"
