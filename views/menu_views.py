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
    receipt_id = request.cookies.get('receipt_id', None)
    table_id = None
    if receipt_id:
        table_id = db.query(f"""SELECT cafe_table.id FROM cafe_table INNER JOIN orders ON
                                            orders.table_id = cafe_table.id INNER JOIN receipt ON
                                            orders.receipt_id = receipt.id WHERE receipt_id = {receipt_id};""", fetch="one")["id"]
        empty_tables = None
    return render_template("menu.html", data=data, tables=empty_tables, table_id=table_id)


def login():
    return render_template('login.html')


def panel():
    # return render_template('panel.html')
    return 'You are Logged'


def order(table_id):
    if request.method == 'GET':
        res = request.cookies
        order_list = db.join_filter(Order, (Receipt, f"id = {res.get('receipt_id', None)}"))

        # order_list = db.join_filter(Order, (Receipt, f"id = {res.get('receipt_id', None)}"))

        data = {'receipt': res.get('receipt_id'),
                'order': order_list}
        return render_template('order.html', data=data)
    elif request.method == 'POST':
        receipt_id = request.cookies.get('receipt_id', None)
        order_dict = request.form
        resp = Response("your order is added!")
        if receipt_id:
            # table_id = db.query("""SELECT cafe_table.id FROM cafe_table INNER JOIN orders ON
            #                             orders.table_id = cafe_table.id INNER JOIN receipt ON
            #                              orders.receipt_id = receipt.id WHERE receipt_id = 5;""", fetch="one")["id"]
            item_id = order_dict.get('item_id')
            number_item = order_dict.get('number_item')
            order1 = Order(item_id=item_id, table_id=table_id,
                           status_id=0, number_item=number_item, receipt_id=receipt_id)
            receipt = db.read(Receipt, int(receipt_id))
            receipt: Receipt
            receipt.total_price += int(number_item) * int(db.read(MenuItems, item_id).price)
            db.update(receipt)
            db.create(order1)
        else:
            price = db.read(MenuItems, int(order_dict.get("item_id"))).price * int(order_dict.get("number_item"))
            receipt = Receipt(total_price=price, final_price=0)
            db.create(receipt)
            order1 = Order(item_id=order_dict.get('item_id'), table_id=order_dict.get('table_id'),
                           status_id=0, number_item=order_dict.get('number_item'), receipt_id=receipt._id)
            db.create(order1)
            resp.set_cookie("receipt_id", f"{receipt._id}", expires=datetime.now() + timedelta(days=1))
            return resp
        return 'good', 201
