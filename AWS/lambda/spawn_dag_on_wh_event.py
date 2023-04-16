import logging

import requests

from creds import *


logging.basicConfig(
    format='[%(levelname)s] %(name)s: %(message)s - %(asctime)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logging.getLogger(name='lambda').setLevel(logging.INFO)


def handler(event=None, context=None):
    url = f'http://{AIRFLOW_API_URL}/api/v1/dags/{DAG_ID_TO_CLONE}/clone/'

    payload = {
        'dag_id': CLONED_DAG_ID,
        'conf': {
            'test_base_dag_args': {
                'user_id': 8431,
                'task_id': 1
            }
        },
    }

    logging.info(f'Cloning Airflow DAG {DAG_ID_TO_CLONE} with custom arguments')
    return requests.get(
        url,
        auth=AIRFLOW_API_AUTH,
        # json=payload,
        headers=AIRFLOW_API_HEADERS
    ).text


print(handler())
