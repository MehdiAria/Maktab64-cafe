from flask import render_template
from core.db_manager import DBManager
from models.model import *
db = DBManager()

def index():
    return render_template("index.html")


def menu():
    items = db.read_all(MenuItems)
    data = {"items": items}
    return render_template("menu.html", data=data)
