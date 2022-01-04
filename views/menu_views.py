from flask import render_template, request, Response
from core.db_manager import DBManager
from models.model import *

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
        db = DBManager()
        if receipt_id:
            order1 = Order(item_id=order_dict.get('item_id'), table_id=order_dict.get('table_id'),
                       status_id=0, number_item=order_dict.get('number_item'), receipt_id=receipt_id)
            db.create(order1)
        else:
            price = db.read(MenuItems, int(order_dict.get("item_id"))).price * int(order_dict.get("number_item"))
            receipt = Receipt(total_price=price, final_price=0)
            db.create(receipt)
            order1 = Order(item_id=order_dict.get('item_id'), table_id=order_dict.get('table_id'),
                           status_id=0, number_item=order_dict.get('number_item'), receipt_id=receipt.id)
            db.create(order1)
        return 'good', 201

