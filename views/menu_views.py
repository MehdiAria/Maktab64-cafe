from flask import render_template
from core.db_manager import DBManager
from models.model import *
db = DBManager()

def index():
    return render_template("index.html")


def menu():
    items = db.read_all(MenuItems)
    print(items)
    data = {"menu_items": items}
    print(data['menu_items'])
    return render_template("menu.html", data=data)
