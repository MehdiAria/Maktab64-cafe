from flask import render_template


def index():
    data = ["static/images/milk_shake.jpg", "static/images/tea.jpg", "static/images/mocha.jpg",
            "static/images/hot_chocolate.jpg"]
    return render_template("index.html", data=data)
