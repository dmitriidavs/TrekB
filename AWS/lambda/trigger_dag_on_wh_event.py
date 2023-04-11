import os
import logging
import datetime as dt
import requests


AIRFLOW_URL = os.environ['AIRFLOW_URL']
DAG_ID = 'trigger_menu_job_dag'


logging.basicConfig(
    format='[%(levelname)s] %(name)s: %(message)s - %(asctime)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logging.getLogger(name='lambda').setLevel(logging.INFO)


def handler(event, context):
    url = f'https://{AIRFLOW_URL}/api/v1/dags/{DAG_ID}/dagRuns'
    payload = {
        'run_id': f'lambda_run_{dt.datetime.utcnow().isoformat()}'
    }
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    logging.info(f'Triggering Airflow DAG {DAG_ID}')
    requests.post(url, data=payload, headers=headers)
