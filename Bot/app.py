"""
TrekB | Smart Portfolio Tracker
:copyright: (c) 2023 by Dmitrii Davletshin (@dmitriidavs)
:license: Apache 2.0, see LICENSE for more details
"""

import uvicorn

from modules.creds import LOCAL_SERVER_HOST, LOCAL_SERVER_PORT
from modules.handlers.webhook import app


if __name__ == '__main__':
    # start local FastAPI server
    uvicorn.run(app, host=LOCAL_SERVER_HOST, port=LOCAL_SERVER_PORT)
