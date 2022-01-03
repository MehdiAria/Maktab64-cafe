from flask import render_template


def about():
    title = "About Us"
    text = """Cafe maktab project created by five passioned maktab students, first phase of the project started a 
    week ago and back in 2020 but that's still in development hoping to be finished within one week and then the team 
    is going to be ready for the second phase of the project. Please let us know whenever you find any bug glitch by 
    opening a ticket on your official github page. """
    img = ""
    date = {
        'title': title,
        'text': text,
    }
    return render_template('about.html', data=date)
