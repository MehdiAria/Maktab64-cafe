from flask import render_template,request
from core.db_manager import DBManager
from models.model import *

db = DBManager()


def index():
    return render_template("index.html")


def menu():
    data = Category.category_item()
    return render_template("menu.html", data=data)

def login():
    return render_template()

# def order(table_id):
#     if request.method=='GET':
#         pass
#     elif request.method=='POST':
