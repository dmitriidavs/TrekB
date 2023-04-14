import logging


logging.basicConfig(
    format='[%(levelname)s]: %(message)s - %(asctime)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(name='basic')
logger.setLevel(logging.INFO)
