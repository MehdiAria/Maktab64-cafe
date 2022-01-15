from flask import render_template, request,redirect, url_for
from utils import get_cashier_by_cookie
def handler():
    if request.args.get('home'):
        render_template("spa/spa-index.html")
    elif request.args.get('about'):
        render_template("spa/spa-about.html")
    elif request.args.get('menu'):
        render_template("spa/spa-menu.html")
    # elif request.args.get('cashier'):
    #     if get_cashier_by_cookie(request):
    #         return redirect('cashier/dashboard.html')
    #     else:
    #         return redirect(url_for('login'))
    #