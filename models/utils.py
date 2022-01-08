# from models.log_1 import logger
import logging
logger = logging.getLogger(__name__)
def number_check(error: type, **kwargs):
    # error: Exception
    error: callable
    for number in kwargs:
        value = kwargs[number]
        try:
            float(value)
        except ValueError:
            logger.error("aklsdaskjdakjd")
            # print('____________________')
            # raise error(number, value)
    return True
