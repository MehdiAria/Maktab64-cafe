import datetime

from flask import render_template, request, escape, redirect, url_for, make_response
from core.db_manager import DBManager
from models.model import Cashier
import uuid, os
from views.utils import get_cashier_by_cookie

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
    # cashiers = db.read_all(Cashier)
    # data = {}
    # data['title'] = "Login Page"
    # data['cashier'] = get_user_by_cookie(request, cashiers)

    if request.method == "GET":
        # form view !
        cashier = get_cashier_by_cookie(request)
        if cashier:
            return render_template('cashier/old_dashboard.html', cashier=cashier)
        error = ''
        return render_template("login.html", error=error)

    elif request.method == "POST":
        # login user
        username = escape(request.form.get('username'))

        password = escape(request.form.get('password'))
        # query = f"""SELECT * FROM cashier WHERE name = \'{str(username)}\' AND password = \'{str(password)}\';"""
        # cashier = db.query(query, 'all')
        res_name = db.read_filter(Cashier, f'name=\'{username}\'')
        res_pass = db.read_filter(Cashier, f'name = \'{str(username)}\' AND password = \'{str(password)}\';')
        try:
            cashier = res_pass[0]

            # check exists cashier !!!
            if cashier.name == username and cashier.password == password:
                # loggin success !
                token = uuid.UUID(bytes=os.urandom(16), version=4)

                cashier.token = str(token)
                db.update(cashier)
                # set cookies
                resp = make_response(redirect(url_for('panel')))
                resp.set_cookie('cashier_logged_in_id', str(cashier.id),
                                expires=datetime.datetime.now() + datetime.timedelta(days=2))
                resp.set_cookie('cashier_logged_in_token', str(token),
                                expires=datetime.datetime.now() + datetime.timedelta(days=2))
                return resp
        except IndexError:
            massage = 'Incorrect username!'
            if res_name:
                massage = 'Incorrect password!'
            error = {
                'error': massage,
            }
            return render_template('login.html', error=error)
        # flash ...
        # redirect (url_for('login'))
        return "Server Error!", 500

    return "Forbidden Request 403", 403
