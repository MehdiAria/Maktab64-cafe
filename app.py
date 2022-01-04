from flask import Flask
from views.menu_views import *
from views.about import *
from views.login import *

app = Flask(__name__, template_folder="templates")

# JINJA_ENVIRONMENT.globals['STATIC_PREFIX'] = '/'


app.add_url_rule("/", "home", index)
app.add_url_rule("/menu", "menu", menu)
app.add_url_rule("/about", "about", about)
app.add_url_rule("/login", "login", login)
app.add_url_rule("/panel", "panel", panel)
app.add_url_rule("/order/<int:table_id>", "order", order, methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(debug=True)
