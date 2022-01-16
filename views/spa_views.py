from flask import render_template, request,redirect, url_for
from views.menu_views import db
from models.model import CafeTable
from models.menu_funcs import menu_categories
def handler():
    if request.args.get('home'):
        return render_template("spa/spa-index.html")
    elif request.args.get('about'):
        return render_template("spa/spa-about.html")
    elif request.args.get('menu'):
        # data = Category.category_item()
        data = {}
        data["menu_items"] = menu_categories()
        empty_tables = None
        table_id = None
        receipt_id = request.cookies.get('receipt_id', None)
        # print(receipt_id)
        if receipt_id:
            table_id = db.query(f"""SELECT cafe_table.id FROM cafe_table INNER JOIN orders ON
                                                orders.table_id = cafe_table.id INNER JOIN receipt ON
                                                orders.receipt_id = receipt.id WHERE receipt_id = {receipt_id};""",
                                fetch="one")["id"]
        else:
            empty_tables = CafeTable.empty_table()
        return render_template("spa/spa-menu.html", receipt_id=receipt_id, data=data, tables=empty_tables, table_id=table_id)


    # elif request.args.get('cashier'):
    #     if get_cashier_by_cookie(request):
    #         return redirect('cashier/dashboard.html')
    #     else:
    #         return redirect(url_for('login'))
    #