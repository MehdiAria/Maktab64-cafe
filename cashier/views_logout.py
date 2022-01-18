from flask import redirect, request, make_response, url_for

def logout():
    resp = make_response(redirect(url_for("login")))
    resp.set_cookie("cashier_logged_in_id", '')
    resp.set_cookie("cashier_logged_in_token", '')
    return resp
