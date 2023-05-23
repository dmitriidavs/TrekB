"""
TrekB | Smart Portfolio Tracker
:copyright: (c) 2023 by Dmitrii Davletshin (@dmitriidavs)
:license: Apache 2.0, see LICENSE for more details
"""

import uvicorn

from modules.handlers.webhook import app


if __name__ == '__main__':
    # start the FastAPI server
    uvicorn.run(app, host="0.0.0.0", port=8000)
