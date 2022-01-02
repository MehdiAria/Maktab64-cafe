from flask import render_template


def index():
    return render_template("index.html")


def menu():
    data = ["static/images/milk_shake.jpg", "static/images/tea.jpg", "static/images/mocha.jpg",
            "static/images/hot_chocolate.jpg"]
    return render_template("menu.html", data=data)
