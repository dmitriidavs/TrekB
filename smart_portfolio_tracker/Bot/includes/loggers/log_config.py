import logging

# TODO: move logging to online dashboard + DB
logging.basicConfig(format='[%(levelname)s]: %(message)s - %(asctime)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

basic_log = logging.getLogger(name='basic')
basic_log.setLevel(logging.INFO)
