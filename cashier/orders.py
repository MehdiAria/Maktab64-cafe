from flask import render_template
from core.db_manager import DBManager
from models.model import Order

db = DBManager()


def orders():
    order_list = db.all_query(Order,
                              f"""SELECT * FROM receipt WHERE time_stamp >= CAST ('{receipt_date_time}' AS timestamp)""")
    data = {'order_list': order_list}
    return render_template('cashier/orders.html', data=data)
