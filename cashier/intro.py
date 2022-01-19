from flask import render_template, request, redirect, url_for
from core.db_manager import DBManager
from datetime import datetime, timedelta

from views.utils import get_cashier_by_cookie

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
        f"SELECT sum(total_price) FROM receipt WHERE is_del=false and is_paid=true and time_stamp BETWEEN CAST ('{today - timedelta(days=1)}' AS timestamp) AND CAST ('{today}' AS timestamp);",
        fetch='one')['sum']
    yesterday_earning = db.query(
        f"SELECT sum(total_price) FROM receipt WHERE is_del=false and is_paid=true and time_stamp BETWEEN CAST ('{today - timedelta(days=2)}' AS timestamp) AND CAST ('{today - timedelta(days=1)}' AS timestamp);",
        fetch='one')['sum']
    yesterday_earning = 1 if yesterday_earning is None else yesterday_earning
    today_earning = 1 if today_earning is None else today_earning
    percent = round((today_earning - yesterday_earning) / yesterday_earning * 100, 2)
    total_orders = db.query(
        f"SELECT count(*) FROM orders WHERE is_del=false;",
        fetch='one')['count']
    new_orders = db.query(
        f"SELECT count(*) FROM orders WHERE is_del=false AND status_id=1;",
        fetch='one')['count']
    cook_orders = db.query(
        f"SELECT count(*) FROM orders WHERE is_del=false AND status_id=2;",
        fetch='one')['count']
    serving_orders = db.query(
        f"SELECT count(*) FROM orders WHERE is_del=false AND status_id=3;",
        fetch='one')['count']
    finished_orders = db.query(
        f"SELECT count(*) FROM orders WHERE is_del=false AND status_id=4;",
        fetch='one')['count']
    if not get_cashier_by_cookie(request):
        return redirect(url_for('panel'))
    return render_template('cashier/intro.html', orders={
        'total_orders': total_orders,
        'new_orders': new_orders,
        'cook_orders': cook_orders,
        'serving_orders': serving_orders,
        'finished_orders': finished_orders,
    }
                           , earning={
            'today_earning': today_earning,
            'yesterday_earning': yesterday_earning,
            'percent': percent,
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
