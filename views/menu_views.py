from flask import render_template


def index():
    data = ["static/"]
    return render_template("index.html")
