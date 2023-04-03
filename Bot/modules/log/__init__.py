__all__ = ['loggers',
           'logger']

import os
import datetime as dt
import logging

from ..creds import BOT_ARCH_TYPE, LOG_FOLDER_PATH, LOG_HOST, LOG_PORT


def create_log_dir() -> bool:
    if not os.path.exists(LOG_FOLDER_PATH):
        os.makedirs(LOG_FOLDER_PATH)
    return True


def gen_filename() -> str:
    return os.path.join('logs', dt.datetime.now().strftime(f'{BOT_ARCH_TYPE}_bot_%Y_%m_%d_%H_%M_%S.log'))


# TODO: create class to add DB logging
logging.basicConfig(
    format='[%(levelname)s]: %(message)s - %(asctime)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    # filename=gen_filename() if BOT_ARCH_TYPE == 'Lite' and create_log_dir() else None
)

logger = logging.getLogger(name='basic')
logger.setLevel(logging.INFO)

if BOT_ARCH_TYPE != 'Lite':
    from logging.handlers import SysLogHandler
    # set logging on external service
    handler = SysLogHandler(address=(LOG_HOST, LOG_PORT))
    logger = logging.getLogger(name='external')
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
