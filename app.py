from flask import Flask, render_template, url_for
from views.menu_views import *

app = Flask(__name__, template_folder="templates")


# JINJA_ENVIRONMENT.globals['STATIC_PREFIX'] = '/'

@app.route('/')
def base():  # put application's code here
    return render_template('base.html')


app.add_url_rule("/index", "home", index)

if __name__ == '__main__':
    app.run(debug=True)
