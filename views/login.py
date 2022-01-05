from flask import render_template, request, escape
from core.db_manager import DBManager
from models.model import *


def login():
    return render_template('login.html')



def register():

    data = {}
    data['title'] = "Register form"
    data['user'] = get_user_by_cookie(request, users)


    if request.method == "GET":
        # form view !
        return render_template("register_view.html", data=data)

    elif request.method == "POST":
        # get user field
        name = escape(request.form.get('name'))
        password = escape(request.form.get('password'))

        for user in users:
            if user['name'] == name:
                return "User exists!", 500

        # register successful !
        user = {
            "id": len(users),
            "name": escape(request.form.get('name')),
            "password": escape(request.form.get('password')),
            "key": '',
        }

        users.append(user)

        return redirect(url_for('home'))

    return "Forbidden Request 403", 403
