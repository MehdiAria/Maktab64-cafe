from flask import Flask, render_template, url_for
from views.menu_views import *
from views.about import *

app = Flask(__name__, template_folder="templates")

# JINJA_ENVIRONMENT.globals['STATIC_PREFIX'] = '/'


app.add_url_rule("/", "home", index)
app.add_url_rule("/menu", "menu", menu)
app.add_url_rule("/about", "about", about)
# app.add_url_rule("/order/<int:table_id>", "order", order, methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(debug=True)
