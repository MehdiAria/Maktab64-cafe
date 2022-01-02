from flask import Flask, render_template, url_for
from views.menu_views import *

app = Flask(__name__, template_folder="templates")


# JINJA_ENVIRONMENT.globals['STATIC_PREFIX'] = '/'



app.add_url_rule("/", "home", index)
app.add_url_rule("/menu", "menu", menu)
if __name__ == '__main__':
    app.run(debug=True)
