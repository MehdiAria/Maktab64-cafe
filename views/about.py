from flask import render_template


def about():
    title = "About Us"
    text = """
    Lorem ipsum dolor sit amet, consectetur adipisicing elit. Amet assumenda delectus doloremque fugit, maiores perferendis quas similique ullam velit vero? Atque excepturi exercitationem illum quia.
    """
    img = ""
    date = {
        'title': title,
        'text': text,
    }
    return render_template('about.html', data=date)
