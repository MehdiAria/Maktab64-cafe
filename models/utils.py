import os


def number_check(error: type, log_path=None, log_skip_path=None, **kwargs):
    error: callable
    from core.logger import create_logger
    if not log_path:
        log_path = os.path.abspath("model.py")
    logger = create_logger(log_path, log_skip_path)
    for key in kwargs:
        number = kwargs[key]
        try:
            float(number)
        except ValueError:
            error = error(field=key, data=number, msg=kwargs.get("msg", ""))
            logger.error(error)
            raise error
    return True
