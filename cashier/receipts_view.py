from flask import render_template
from core.db_manager import DBManager
from models.model import Receipt
from datetime import datetime, timedelta

db = DBManager()


def time_receipts(time_filter=0):
    receipt_date_time = datetime.now() - timedelta(hours=time_filter)
    data = db.all_query(Receipt, f"""SELECT * FROM receipt WHERE time_stamp >= CAST ('{receipt_date_time}' AS timestamp)""")
    return render_template("cashier/receipts.html", data=data)

