from flask import render_template
from core.db_manager import DBManager
from models.model import CafeTable


db = DBManager()


def tables():
    tables = db.read_all(CafeTable)
    return render_template('cashier/tables.html', data=tables)