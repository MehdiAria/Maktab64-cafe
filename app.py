from flask import Flask
from views.menu_views import *
from views.about import *
from views.login import *
from cashier import tables
from cashier import orders
from cashier import edit_items
from cashier.receipts_view import *

app = Flask(__name__, template_folder="templates")

# JINJA_ENVIRONMENT.globals['STATIC_PREFIX'] = '/'


app.add_url_rule("/", "home", index)
app.add_url_rule("/menu", "menu", menu)
app.add_url_rule("/about", "about", about)
app.add_url_rule("/login", "login", login, methods=['GET', 'POST'])
app.add_url_rule("/panel", "panel", panel)
app.add_url_rule("/order/<string:table_id>", "order", order, methods=['GET', 'POST'])
app.add_url_rule("/deldec/", "deldec", orders.deldec, methods=['GET', 'POST'])
app.add_url_rule("/cashier/edit_items", "edit_items", edit_items.edit_items, methods=['GET', 'POST'])
app.add_url_rule("/cashier/orders", "orders", orders.orders, methods=['GET', 'POST'])
app.add_url_rule("/cashier/receipts", "date_receipts", all_receipts, methods=["GET", "POST"])
# app.add_url_rule("cashier/served_orders", "served_orders", served_orders)
app.add_url_rule("/cashier/tables", "tables", tables.tables, methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(debug=True)
