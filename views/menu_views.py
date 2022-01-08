from flask import render_template, request, Response
from core.db_manager import DBManager
from models.model import *
from datetime import datetime, timedelta
import uuid, os

db = DBManager()


def index():
    return render_template("index.html")


def menu():
    data = Category.category_item()
    empty_tables = None
    table_id = None
    receipt_id = request.cookies.get('receipt_id', None)
    if receipt_id:
        table_id = db.query(f"""SELECT cafe_table.id FROM cafe_table INNER JOIN orders ON
                                            orders.table_id = cafe_table.id INNER JOIN receipt ON
                                            orders.receipt_id = receipt.id WHERE receipt_id = {receipt_id};""",
                            fetch="one")["id"]
    else:
        empty_tables = CafeTable.empty_table()
    return render_template("menu.html", data=data, tables=empty_tables, table_id=table_id)


def login():
    return render_template('login.html')


def panel():
    # if request.cookies.get()

    # return render_template('panel.html')
    return 'You are Logged'


def order(table_id):
    table = db.read(CafeTable, int(table_id))
    table: CafeTable
    if request.method == 'GET':
        res = request.cookies
        order_list = db.join_filter(Order, (Receipt, f"id = {res.get('receipt_id', None)}"))
        order_item = dict()
        for i in order_list:
            i: Order
            order_item[i] = db.read(MenuItems, i.item_id)
        # item_list = db.all_query(MenuItems,
        #                          f"SELECT menu_items.id,menu_items.category_id,discount,menu_items.name,price,image_url,serving_time FROM menu_items INNER JOIN orders on orders.item_id=menu_items.id;")
        price_list = db.all_query(Receipt,
                                  f"SELECT * FROM receipt where id={res.get('receipt_id', None)};")

        data = {'receipt': res.get('receipt_id'),
                'order': order_list, 'item': order_item, 'price': price_list[0]}
        return render_template('order.html', data=data)
    elif request.method == 'POST':
        receipt_id = request.cookies.get('receipt_id', None)
        user_token = request.cookies.get("user_token", None)
        order_dict = request.form
        resp = Response("your order is added!", status=201)
        if receipt_id and user_token:
            item_id = order_dict.get('item_id', None)
            number_item = order_dict.get('number_item', None)
            table_order = Order(item_id=item_id, table_id=table_id,
                                status_id=0, number_item=number_item, receipt_id=receipt_id)
            db.create(table_order)
            receipt = db.read_filter(Receipt, f"id = {receipt_id} AND user_token = \'{user_token}\'")[0]  # TODO handel erroe in reading receipt
            receipt: Receipt
            receipt.total_price += int(number_item) * int(db.read(MenuItems, item_id).price)
            new_token = str(uuid.UUID(bytes=os.urandom(16)))
            receipt.user_token = new_token
            db.update(receipt)
            resp.set_cookie("user_token", new_token),  # TODO set user_token for anyone
            return resp, 201

        else:
            assert table and (table.is_empty or user_token)
            price = db.read(MenuItems, int(order_dict.get("item_id"))).price * int(order_dict.get("number_item"))
            if user_token:
                receipt = db.read_filter(Receipt, f"user_token = \'{user_token}\'")[0]  # TODO handel error in reading receipt!
            else:
                receipt = Receipt(total_price=price, final_price=0)
                db.create(receipt)
                token = str(uuid.UUID(bytes=os.urandom(16)))
                receipt.user_token = token
            table_order = Order(item_id=order_dict.get('item_id'), table_id=table_id,
                                status_id=0, number_item=order_dict.get('number_item'), receipt_id=receipt._id)
            db.create(table_order)
            resp.set_cookie("receipt_id", f"{receipt._id}", expires=datetime.now() + timedelta(days=1))
            new_token = str(uuid.UUID(bytes=os.urandom(16)))
            resp.set_cookie("user_token", new_token),  # TODO set user_token for anyone
            receipt.user_token = new_token
            db.update(receipt)
            return resp
    return 'server error', 403
