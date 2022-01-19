from flask import render_template, request, redirect, url_for
from core.db_manager import DBManager
from models.model import Receipt
from datetime import datetime, timedelta

from views.utils import get_cashier_by_cookie

db = DBManager()


# def time_receipts(time_filter=0):
#     date_time = datetime.now() - timedelta(days=time_filter)
#     data = db.all_query(Receipt, f"""SELECT * FROM receipt WHERE time_stamp >= CAST ('{date_time}' AS timestamp)""")
#     print(data)
#     print(len(data))
#     return render_template("cashier/receipts.html", data=data)


def all_receipts():
    if not get_cashier_by_cookie(request):
        return redirect(url_for('panel'))
    if request.method == "POST":
        receipt_dict = request.form
        receipt = db.read(Receipt, int(receipt_dict.get("_id")))
        receipt: Receipt
        receipt.is_del = True if receipt_dict.get("is_del") == "true" else False
        receipt.is_paid = True if receipt_dict.get("is_paid") == "true" else False
        receipt.final_price = receipt_dict.get('final_price')
        db.update(receipt)
        return "Edit was successful!"
    data = db.read_all(Receipt)
    return render_template("cashier/receipts.html", data=data)

