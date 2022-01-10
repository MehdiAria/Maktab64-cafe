from flask import render_template
from core.db_manager import DBManager
from models.model import Order
from datetime import datetime

db = DBManager()


def orders():
    order_list = db.all_query(Order,
                              f"""SELECT * FROM orders WHERE True;""")
    datetime_list = list(
        map(lambda x: datetime.strptime('T'.join(x.time_stamp.__str__().split()), '%Y-%m-%dT%H:%M:%S.%f'), order_list))
    data = {'order_list': order_list, 'datetime_list': datetime_list}
    return render_template('cashier/orders.html', data=data)
