from flask import render_template, request, Response, redirect, url_for, escape
from models.model import *
from datetime import datetime, timedelta
from views.utils import set_user_token, check_table_id, get_cashier_by_cookie, order_operation
from models.menu_funcs import menu_categories
from core.logger import create_logger

logger = create_logger(__file__, file_skip=0)
db = DBManager()


def index():
    return render_template("index.html")


def menu():
    data = {}
    data["menu_items"] = menu_categories()
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
    return render_template("menu.html", receipt_id=receipt_id, data=data, tables=empty_tables, table_id=table_id)


def panel():
    cashier = get_cashier_by_cookie(request)
    if cashier:
        return render_template('cashier/dashboard.html', data=cashier[0])
    else:
        return redirect(url_for('login'))


def order(table_id):
    """
    :param table_id:
    POST:
        gets table_id from url, (item_id & number_item) from html from
        if the user has not user_token and receipt_id it would create a receipt for that user
        :return Response with no template
    GET:
        :return renders a html file to show user orders
    """
    if request.method == 'GET':
        receipt_id = request.cookies.get('receipt_id', None)
        data = {"error": "you have no orders!"}
        if receipt_id:
            order_list = db.all_query(Order,
                                      f"SELECT orders.id, orders.item_id, orders.number_item, orders.receipt_id, orders.status_id, orders.table_id, orders.time_stamp FROM orders inner join receipt on orders.receipt_id=receipt.id where receipt.is_del=false and orders.is_del=false and receipt_id = {receipt_id} ;")
            order_item = dict()
            for i in order_list:
                i: Order
                order_item[i] = db.read(MenuItems, i.item_id)
            price_list = db.all_query(Receipt,
                                      f"SELECT * FROM receipt where id={receipt_id} and receipt.is_del = false;")
            # price_list_2 = db.read_filter(Receipt,f"id= {receipt_id} AND is_del = false")
            data = {'receipt': receipt_id, 'order': order_list, 'item': order_item, 'price': price_list[0],
                    "error": None}

        return render_template('order.html', data=data)
    elif request.method == 'POST':
        receipt_id = request.cookies.get('receipt_id', None)
        user_token = request.cookies.get("user_token", None)
        order_dict = request.form
        resp = Response("your order is added!", status=201)
        if receipt_id and user_token:
            item_id = escape(order_dict.get('item_id', None))
            number_item = escape(order_dict.get('number_item', None))
            check_table_id(receipt_id, table_id)
            table_order = Order(item_id=item_id, table_id=table_id,
                                status_id=1, number_item=number_item, receipt_id=receipt_id)
            db.create(table_order)
            receipt = db.read_filter(Receipt, f"id = {receipt_id} AND user_token = \'{user_token}\'")[0]
            # TODO handel error in reading receipt
            receipt: Receipt
            price = int(number_item) * int(db.read(MenuItems, item_id).price)
            receipt.total_price += price
            receipt.final_price += price
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
                receipt = Receipt(total_price=price, final_price=price)
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
    """
    updates (set is_del = true) order, receipt using order_id
    :return: a Response object has delete cookie if there is just one order
    """
    if request.method == 'POST':
        receipt_id = request.cookies.get('receipt_id', None)
        order_id = request.form.get('order_id')
        receipt = db.read_filter(Receipt, f"id = {receipt_id}", fetch="one")
        orders = db.read_filter(Order, f"receipt_id = {request.cookies.get('receipt_id', None)} And is_del=false")
        count = int(request.form.get("number_item"))
        pr = int(request.form.get("item_price"))
        price_decrease = count * pr
        print("delete -> ",price_decrease, "count",count, "price", pr)
        receipt.total_price -= price_decrease
        receipt.final_price -= price_decrease
        db.update(receipt)
        logger.warning(f"changed total_price of {receipt_id} with {order_id} -> {receipt.total_price}")
        resp = Response(f"{receipt.total_price},{receipt.final_price}", status=201)
        if orders and len(orders) == 1:
            receipt.is_del = True
            db.update(receipt)
            resp.delete_cookie("receipt_id")
            resp.delete_cookie("user_token")
            table = db.all_query(CafeTable,
                                 f"SELECT {CafeTable.class_aliases(to_str=True)} FROM cafe_table  INNER JOIN orders on orders.table_id = cafe_table.id WHERE orders.id = {order_id}",
                                 fetch="one")
            table.is_empty = True
            db.update(table)
        table_order = db.read(Order, order_id)
        table_order.is_del = True
        db.update(table_order)
        return resp


def dec_order():
    if request.method == 'POST':
        return order_operation(request, "-")


def plus_order():
    if request.method == 'POST':
        return order_operation(request, "+")


def check_out_order():
    if request.method == "GET":
        receipt_id = request.cookies.get("receipt_id", None)
        receipt = db.read(Receipt, receipt_id)
        discount = db.query(
            f"SELECT sum(menu_items.discount) as discount_plus from orders INNER join menu_items on orders.item_id = menu_items.id where orders.receipt_id = {receipt_id} and orders.status_id =1",
            fetch="one")["discount_plus"]
        receipt.final_price -= int(discount)
        db.update(receipt)
        if receipt_id:
            db.query(
                f"UPDATE orders SET status_id = 2 WHERE orders.receipt_id = {receipt_id} AND orders.is_del = false AND orders.status_id = 1")
            return {"total_price": receipt.total_price, "final_price": receipt.final_price}
