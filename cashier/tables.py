from flask import render_template,request
from core.db_manager import DBManager
from models.model import CafeTable


db = DBManager()


def tables():
    tables = db.read_all(CafeTable)
    if request.method =='GET':
        return render_template('cashier/tables.html', data=tables)
    elif request.method =='POST':
        # print('data:', request.form.get())
        table = db.read(CafeTable, request.form.get('_id'))
        table.is_del = True if request.form.get('is_del') == 'true' else False
        table.space = request.form.get('space')
        table.is_empty = request.form.get('is_empty')
        db.update(table)
        return "change is done!"

def add_table():
    if request.method == 'POST':
        space = request.form.get('space')
        new_table = CafeTable(False, False, space)
        db.create(new_table)
        return 'add table success!'

def del_table():
    if request.method == 'POST':
        table = db.read(CafeTable, request.form.get('_id'))
        table.is_del = True
        db.update(table)
        return 'delete table success!'
