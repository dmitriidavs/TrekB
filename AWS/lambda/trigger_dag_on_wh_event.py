import os
import logging
import datetime as dt
import requests


AIRFLOW_URL = os.environ['AIRFLOW_URL']
AUTH = (os.environ['AIRFLOW_USR'], os.environ['AIRFLOW_PWD'])
DAG_NAME = 'test_api_dag_1'


logging.basicConfig(
    format='[%(levelname)s] %(name)s: %(message)s - %(asctime)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logging.getLogger(name='lambda').setLevel(logging.INFO)


def handler(event=None, context=None):
    url = f'http://{AIRFLOW_URL}/api/v1/dags/{DAG_NAME}/dagRuns'

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    payload = {
        'conf': {},
    }

    logging.info(f'Triggering Airflow DAG {DAG_NAME}')
    return requests.post(url, auth=AUTH, json=payload, headers=headers).text


print(handler())
