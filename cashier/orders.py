from flask import render_template, request, redirect, url_for
from core.db_manager import DBManager
from models.model import Order, Status
from views.utils import get_cashier_by_cookie

db = DBManager()


def orders():
    order_list = db.query(
        f"SELECT {Order.class_aliases(to_str=True)},menu_items.name as item_name,status.name as status_name FROM orders INNER JOIN status ON orders.status_id=status.id INNER JOIN menu_items ON menu_items.id=orders.item_id;",
        fetch='all')
    # print(order_list)
    status_list = db.all_query(Status,
                               f"SELECT * FROM status where True;")
    # order_list = db.query(
    #     f"""-- SELECT * FROM orders INNER JOIN status ON orders.status_id=status.id INNER JOIN menu_items ON menu_items.id=orders.item_id;""")
    # datetime_list = list(
    #     map(lambda x: 'T'.join(x.time_stamp.__str__().split()), order_list))
    # data = zip(order_list, datetime_list)
    if request.method == 'GET':
        if not get_cashier_by_cookie(request):
            return redirect(url_for('panel'))
        return render_template('cashier/orders.html', status=status_list, data=order_list)
    elif request.method == 'POST':
        order = db.read(Order, int(request.form.get('_id')))
        order.is_del = True if request.form.get('is_del') == 'true' else False
        # order.item_id = request.form.get('item_id')
        order.number_item = request.form.get('number_item')
        status_name = request.form.get('status_name')
        st = db.read_filter(Status, f"name=\'{status_name}\'")[0].id
        order.status_id = st
        db.update(order)
        return "Edit was successful!"
