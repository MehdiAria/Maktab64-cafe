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
    return render_template("menu.html", data=data, tables=empty_tables)


def login():
    return render_template('login.html')


def panel():
    return render_template('panel.html')


def order(table_id):
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        # return Response('Your order created!', 201)
        receipt_id = request.cookies.get('receipt_id', None)
        order_dict = request.form
        # item = db.read(MenuItems, int(order_dict.get("item_id")))
        print(order_dict)
        print(request.form)
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
