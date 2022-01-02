from flask import Flask, render_template, url_for




app = Flask(__name__, template_folder="templates")

# JINJA_ENVIRONMENT.globals['STATIC_PREFIX'] = '/'

@app.route('/')
def base():  # put application's code here
    return render_template('base.html')


if __name__ == '__main__':
    app.run(debug=True)
