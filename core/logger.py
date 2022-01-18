import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s %(levelname)s:%(message)s')


def create_logger(file, file_skip=None):
    file: str
    if file_skip:
        assert isinstance(file_skip, int)
        skip_number = -file_skip
        return logging.getLogger("/".join(file.split("/")[skip_number:-1]))
    return logging.getLogger(file)
