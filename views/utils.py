def get_user_by_cookie(request, users: list):
    user_id = request.cookies.get('user_logged_in_id', None)
    user_key = request.cookies.get('user_logged_in_key', None)

    print(user_id, user_key)

    for user in users:
        if user['key'] == user_key and str(user['id']) == user_id:
            return user

    return None