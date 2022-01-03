from flask import render_template


def about():
    title = "About Us"
    text = """ """
    img = ""
    date = {
        'title': title,
        'text': text,
    }
    return render_template('about.html', data=date)
