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
        return 'ok',201
