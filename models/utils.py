def number_check(error: type, **kwargs):
    error: callable
    for key in kwargs:
        number = kwargs[key]
        try:
            float(number)
        except ValueError:
            raise error(field=key, data=number, msg=kwargs.get("msg", ""))
    return True
