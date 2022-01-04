from flask import render_template, request, Response
from core.db_manager import DBManager
from models.model import *
from datetime import datetime, timedelta

db = DBManager()


def index():
    return render_template("index.html")


def menu():
    data = Category.category_item()
    empty_tables = CafeTable.empty_table()
    table_id = None
    user_table_id = request.cookies.get('table_id', None)
    if user_table_id:
        table_id = table_id
        empty_tables = None
    return render_template("menu.html", data=data, tables=empty_tables, table_id=table_id)


def login():
    return render_template('login.html')


def panel():
    return render_template('panel.html')


def order(table_id):
    if request.method == 'GET':
        res = request.cookies
        # print(res)
        order_list = db.read_filter_nowhere(Order,
                                            f"SELECT orders.id, item_id, number_item, receipt_id, status_id, table_id FROM orders INNER JOIN receipt ON orders.receipt_id={res['receipt_id']};")

        data = {'receipt': res.get('receipt_id'),
                'order': order_list}
        return render_template('order.html', data=data)
    elif request.method == 'POST':
        # return Response('Your order created!', 201)
        receipt_id = request.cookies.get('receipt_id', None)
        order_dict = request.form
        # item = db.read(MenuItems, int(order_dict.get("item_id")))
        resp = Response("your order is added!")
        resp.set_cookie("table_id", order_dict.get("table_id"))
        if receipt_id:
            order1 = Order(item_id=order_dict.get('item_id'), table_id=order_dict.get('table_id'),
                           status_id=0, number_item=order_dict.get('number_item'), receipt_id=receipt_id)
            db.create(order1)
        else:
            price = db.read(MenuItems, int(order_dict.get("item_id"))).price * int(order_dict.get("number_item"))
            receipt = Receipt(total_price=price, final_price=0)
            db.create(receipt)
            order1 = Order(item_id=order_dict.get('item_id'), table_id=order_dict.get('table_id'),
                           status_id=0, number_item=order_dict.get('number_item'), receipt_id=receipt._id)
            db.create(order1)
            resp = Response("your order is added!")
            resp.set_cookie("receipt_id", f"{receipt._id}", expires=datetime.now()+timedelta(days=1))
            return resp
        return 'good', 201
