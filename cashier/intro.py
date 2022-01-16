from flask import render_template, request
from core.db_manager import DBManager
from datetime import datetime, timedelta

db = DBManager()


def intro():
    total_tables = db.query("SELECT count(*) FROM cafe_table;", fetch='one')['count']
    available_tables = db.query("SELECT count(*) FROM cafe_table WHERE is_del=false AND is_empty=true;", fetch='one')[
        'count']
    deleted_tables = db.query("SELECT count(*) FROM cafe_table WHERE is_del=true;", fetch='one')['count']
    reserved_tables = db.query("SELECT count(*) FROM cafe_table WHERE is_empty=false;", fetch='one')['count']
    return render_template('cashier/intro.html', tables_data={
        'total_tables': total_tables,
        'available_tables': available_tables,
        'deleted_tables': deleted_tables,
        'reserved_tables': reserved_tables,
    })
