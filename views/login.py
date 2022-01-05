from flask import render_template, request, escape, redirect, url_for
from core.db_manager import DBManager
from models.model import Cashier
from views.utils import get_user_by_cookie
import uuid, os

db = DBManager()


# def register():
#
#     cashiers = db.read_all(Cashier)
#     data = {}
#     data['title'] = "Register Page"
#     data['cashier'] = get_user_by_cookie(request, cashiers)
#
#
#     if request.method == "GET":
#         # form view !
#         return render_template("register_view.html", data=data)
#
#     elif request.method == "POST":
#         # get user field
#         name = escape(request.form.get('name'))
#         last_name = escape(request.form.get('last_name'))
#         email = escape(request.form.get('email'))
#         phone = escape(request.form.get('phone'))
#         password = escape(request.form.get('password'))
#
#         for cashier in cashiers:
#             if cashier['name'] == name:
#                 return "User exists!", 500
#         token = uuid.UUID(bytes=os.urandom(16), version=4)
#         # register successful !
#         cashier = Cashier(name, last_name, email, phone, password, token)
#         db.create(cashier)
#
#         return redirect(url_for('panel'))
#
#     return "Forbidden Request 403", 403

def login():

    cashiers = db.read_all(Cashier)
    data = {}
    data['title'] = "Login Page"
    data['cashier'] = get_user_by_cookie(request, cashiers)

    if request.method == "GET":
        # form view !
        return render_template("login.html", data=data)

    elif request.method == "POST":
        # login user
        name = escape(request.form.get('name'))
        password = escape(request.form.get('password'))
        cashiers = db.read_all(Cashier)

        # check exists cashier !!!
        for cashier in cashiers:
            if cashier.name == name and cashier.password == password:
                # loggin success !
                token = uuid.UUID(bytes=os.urandom(16), version=4)
                cashier.token = token
                db.update(cashier)

