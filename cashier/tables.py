from flask import render_template,request
from core.db_manager import DBManager
from models.model import CafeTable


db = DBManager()


def tables():
    tables = db.read_all(CafeTable)
    if request.method =='GET':
        return render_template('cashier/tables.html', data=tables)
    elif request.method =='POST':
        # print(request.form.get('space'))
        return request.form.get('space')