from flask import render_template


def orders():
    return render_template('cashier/orders.html')
