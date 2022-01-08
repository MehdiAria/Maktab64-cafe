def number_check(error: type, **kwargs):
    # error: Exception
    error: callable
    for number in kwargs:
        value = kwargs[number]
        try:
            float(value)
        except ValueError:
            raise error(number, value)
    return True
