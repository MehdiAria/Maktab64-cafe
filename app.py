from flask import Flask
from views.menu_views import *
from views.about import *
from views.login import *
from cashier import tables, orders, edit_items, intro
from cashier.receipts_view import *
from cashier.views_logout import *
from models.menu_funcs import menu_categories
from views.spa_views import handler
app = Flask(__name__, template_folder="templates")

# JINJA_ENVIRONMENT.globals['STATIC_PREFIX'] = '/'

@app.route("/mn_2")
def new_menu():
    data = {}
    data["menu_items"] = menu_categories()
    print(data)
    return render_template("items.html", data=data)

app.add_url_rule("/", "home", index)
app.add_url_rule("/menu", "menu", menu)
app.add_url_rule("/about", "about", about)
app.add_url_rule("/login", "login", login, methods=['GET', 'POST'])
app.add_url_rule("/panel", "panel", panel)
app.add_url_rule("/order/<string:table_id>", "order", order, methods=['GET', 'POST'])
app.add_url_rule("/delete", "delete", del_order, methods=['GET', 'POST'])
app.add_url_rule("/decrease", "decrease", dec_order, methods=['GET', 'POST'])
app.add_url_rule("/order-plus", "plus_order", plus_order, methods=['GET', 'POST'])
app.add_url_rule("/cashier/edit_items", "edit_items", edit_items.edit_items, methods=['GET', 'POST'])
app.add_url_rule("/cashier/orders", "orders", orders.orders, methods=['GET', 'POST'])
app.add_url_rule("/cashier/receipts", "date_receipts", all_receipts, methods=["GET", "POST"])
app.add_url_rule("/cashier/intro", "intro", intro.intro, methods=["GET", "POST"])
app.add_url_rule("/cashier/tables", "tables", tables.tables, methods=['GET', 'POST'])
app.add_url_rule("/cashier/add_table", "add_table", tables.add_table, methods=['GET', 'POST'])
app.add_url_rule("/cashier/del_table", "del_table", tables.del_table, methods=['GET', 'POST'])
app.add_url_rule("/check_out_order", "check_out_order", check_out_order, methods=['GET', 'POST']) # TODO not POST
app.add_url_rule("/cashier/logout", 'logout', logout)
app.add_url_rule("/handler", 'handler', handler)
if __name__ == '__main__':
    app.run(debug=True)
