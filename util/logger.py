import logging


internal_logger = logging.getLogger('Marvin')
internal_logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler('marvin.log')
fh.setLevel(logging.ERROR)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
internal_logger.addHandler(fh)
internal_logger.addHandler(ch)

def log(message, level = logging.DEBUG):
    internal_logger.log(level, message)

