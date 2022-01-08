import os


def number_check(error: type, file_path=None, **kwargs, ):
    error: callable
    from models.logger_1 import create_logger
    if not file_path:
        file_path = os.path.abspath("model.py")
    logger = create_logger(file_path)
    for key in kwargs:
        number = kwargs[key]
        try:
            float(number)
        except ValueError:
            error = error(field=key, data=number, msg=kwargs.get("msg", ""))
            logger.error(error)
            raise error
    return True
