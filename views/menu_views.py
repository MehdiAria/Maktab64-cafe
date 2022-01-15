from flask import render_template, request, Response, redirect, url_for
from core.db_manager import DBManager
from models.model import *
from datetime import datetime, timedelta
import uuid, os
from views.utils import set_user_token, check_table_id, get_cashier_by_cookie
from models.menu_funcs import menu_categories

db = DBManager()


def index():
    return render_template("index.html")


def menu():
    # data = Category.category_item()
    data = {}
    data["menu_items"] = menu_categories()
    empty_tables = None
    table_id = None
    receipt_id = request.cookies.get('receipt_id', None)
    # print(receipt_id)
    if receipt_id:
        table_id = db.query(f"""SELECT cafe_table.id FROM cafe_table INNER JOIN orders ON
                                            orders.table_id = cafe_table.id INNER JOIN receipt ON
                                            orders.receipt_id = receipt.id WHERE receipt_id = {receipt_id};""",
                            fetch="one")["id"]
    else:
        empty_tables = CafeTable.empty_table()
    return render_template("menu.html", receipt_id=receipt_id, data=data, tables=empty_tables, table_id=table_id)


def panel():
    if get_cashier_by_cookie(request):
        return render_template('cashier/dashboard.html')
    else:
        return redirect(url_for('login'))


def order(table_id):
    if request.method == 'GET':
        res = request.cookies
        # order_list = db.join_filter(Order, (Receipt, f"id = {res.get('receipt_id', None)}"))
        order_list = db.all_query(Order,
                                  f"SELECT orders.id, orders.item_id, orders.number_item, orders.receipt_id, orders.status_id, orders.table_id, orders.time_stamp FROM orders inner join receipt on orders.receipt_id=receipt.id where receipt.is_del=false and orders.is_del=false ;")
        order_item = dict()
        for i in order_list:
            i: Order
            order_item[i] = db.read(MenuItems, i.item_id)
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
            check_table_id(receipt_id, table_id)
            table_order = Order(item_id=item_id, table_id=table_id,
                                status_id=1, number_item=number_item, receipt_id=receipt_id)
            db.create(table_order)
            receipt = db.read_filter(Receipt, f"id = {receipt_id} AND user_token = \'{user_token}\'")[0]
            # TODO handel error in reading receipt
            receipt: Receipt
            receipt.total_price += int(number_item) * int(db.read(MenuItems, item_id).price)
            new_token = set_user_token(receipt)
            resp.set_cookie("user_token", new_token)
            return resp, 201
        else:
            table = db.read(CafeTable, int(table_id))
            table: CafeTable
            assert table and (table.is_empty or user_token)
            price = db.read(MenuItems, int(order_dict.get("item_id"))).price * int(order_dict.get("number_item"))
            if user_token:
                receipt = db.read_filter(Receipt, f"user_token = \'{user_token}\'")[
                    0]  # TODO handel error in reading receipt!
            else:
                receipt = Receipt(total_price=price, final_price=0)
                db.create(receipt)
            table_order = Order(item_id=order_dict.get('item_id'), table_id=table_id,
                                status_id=1, number_item=order_dict.get('number_item'), receipt_id=receipt._id)
            resp.set_cookie("receipt_id", f"{receipt._id}", expires=datetime.now() + timedelta(days=1))
            db.create(table_order)
            new_token = set_user_token(receipt)
            resp.set_cookie("user_token", new_token),  # TODO set user_token for anyone
            table.is_empty = False
            db.update(table)
            return resp
    return 'server error', 403

def del_order():
    if request.method == 'POST':
        x = request.form.get('order_id')
        obj_order = db.read(Order, x)
        db.delete(obj_order)
        return "order deleted"


def dec_order():
    if request.method == 'POST':
        x = int(request.form.get('order_id')[3:])
        obj_order = db.read(Order, x)
        obj_order.number_item = obj_order.number_item - 1
        db.update(obj_order)
        return {'number_item': obj_order.number_item, "order_id": obj_order.id}
