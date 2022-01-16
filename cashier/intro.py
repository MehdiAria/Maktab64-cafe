from flask import render_template, request
from core.db_manager import DBManager
from datetime import datetime, timedelta

db = DBManager()


def intro():
    available_tables = db.query("SELECT count(*) FROM cafe_table WHERE is_del=false AND is_empty=true;", fetch='one')[
        'count']
    deleted_tables = db.query("SELECT count(*) FROM cafe_table WHERE is_del=true;", fetch='one')['count']
    reserved_tables = db.query("SELECT count(*) FROM cafe_table WHERE is_empty=false;", fetch='one')['count']
    today = datetime.now()
    receipt_5 = db.query(
        f"SELECT count(*) FROM receipt WHERE time_stamp BETWEEN CAST ('{today - timedelta(days=5)}' AS timestamp) AND CAST ('{today - timedelta(days=4)}' AS timestamp);",
        fetch='one')['count']
    receipt_4 = db.query(
        f"SELECT count(*) FROM receipt WHERE time_stamp BETWEEN CAST ('{today - timedelta(days=4)}' AS timestamp) AND CAST ('{today - timedelta(days=3)}' AS timestamp);",
        fetch='one')['count']
    receipt_3 = db.query(
        f"SELECT count(*) FROM receipt WHERE time_stamp BETWEEN CAST ('{today - timedelta(days=3)}' AS timestamp) AND CAST ('{today - timedelta(days=2)}' AS timestamp);",
        fetch='one')['count']
    receipt_2 = db.query(
        f"SELECT count(*) FROM receipt WHERE time_stamp BETWEEN CAST ('{today - timedelta(days=2)}' AS timestamp) AND CAST ('{today - timedelta(days=1)}' AS timestamp);",
        fetch='one')['count']
    receipt_1 = db.query(
        f"SELECT count(*) FROM receipt WHERE time_stamp BETWEEN CAST ('{today - timedelta(days=1)}' AS timestamp) AND CAST ('{today - timedelta(days=0)}' AS timestamp);",
        fetch='one')['count']
    today_earning = db.query(
        f"SELECT sum(total_price) FROM receipt WHERE time_stamp BETWEEN CAST ('{today - timedelta(days=1)}' AS timestamp) AND CAST ('{today - timedelta(days=0)}' AS timestamp);",
        fetch='one')['sum']
    yesterday_earning = db.query(
        f"SELECT sum(total_price) FROM receipt WHERE time_stamp BETWEEN CAST ('{today - timedelta(days=3)}' AS timestamp) AND CAST ('{today - timedelta(days=2)}' AS timestamp);",
        fetch='one')['sum']
    return render_template('cashier/intro.html', earning={
        'today_earning': today_earning,
        'yesterday_earning': yesterday_earning,
    },
                           tables_data={
                               'available_tables': available_tables,
                               'deleted_tables': deleted_tables,
                               'reserved_tables': reserved_tables,
                           }, receipt_data={
            'receipt_1': receipt_1,
            'receipt_2': receipt_2,
            'receipt_3': receipt_3,
            'receipt_4': receipt_4,
            'receipt_5': receipt_5,
        })
