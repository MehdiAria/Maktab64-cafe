def get_user_by_cookie(request, cashiers: list):
    cashier_id = request.cookies.get('cashier_logged_in_id', None)
    cashier_token = request.cookies.get('cashier_logged_in_key', None)

    print(cashier_id, cashier_token)

    for cashier in cashiers:
        if cashier.token == cashier_token and cashier.id == cashier_id:
            return cashier

    return None