from flask import render_template, request
from core.db_manager import DBManager
from models.model import Receipt
from datetime import datetime, timedelta

db = DBManager()


# def time_receipts(time_filter=0):
#     date_time = datetime.now() - timedelta(days=time_filter)
#     data = db.all_query(Receipt, f"""SELECT * FROM receipt WHERE time_stamp >= CAST ('{date_time}' AS timestamp)""")
#     print(data)
#     print(len(data))
#     return render_template("cashier/receipts.html", data=data)


def all_receipts():
    if request.method == "POST":
        return "good!"
    data = db.read_all(Receipt)
    return render_template("cashier/receipts.html", data=data)
