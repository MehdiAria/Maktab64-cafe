from flask import render_template,request
from core.db_manager import DBManager
from models.model import CafeTable


db = DBManager()


def tables():
    tables = db.read_all(CafeTable)
    if request.method =='GET':
        return render_template('cashier/tables.html', data=tables)
    elif request.method =='POST':
        print('data:', request.get_json(force=True))
        table = db.read(CafeTable, int(request.form.get('_id')))
        table.is_del = True if request.form.get('is_del') == 'true' else False
        table.space = request.form.get('space')
        table.is_empty = request.form.get('is_empty')
        db.update(table)
        return "success"