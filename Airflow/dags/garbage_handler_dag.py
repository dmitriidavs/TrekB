import datetime as dt

import requests
from requests.exceptions import HTTPError
from airflow.models import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

from includes.creds import *
from includes.utils.log import logger


args = {
    'owner': 'dmitriidavs',
    'start_date': dt.datetime(2023, 4, 13, 10, 0, 0, 0),
    'retries': 2,
    'retry_delay': dt.timedelta(minutes=3),
    'depends_on_past': False,
}


def get_data(url: str) -> dict:
    """Get data from Airflow API"""

    response = requests.get(url,
                            auth=AIRFLOW_API_AUTH,
                            headers=AIRFLOW_API_HEADERS)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPError(f'{url}: Failed fetching url. Response:\n{response.text}')


def delete_dag_data(dag_id: str) -> None:
    """Delete dag from UI and metabase"""

    url = f'http://{AIRFLOW_API_URL}/api/v1/dags/{dag_id}'
    response = requests.delete(url,
                               auth=AIRFLOW_API_AUTH,
                               headers=AIRFLOW_API_HEADERS)

    if response.status_code == 204:
        logger.info(f'{dag_id}: Deleted DAG')
    else:
        raise HTTPError(f'{dag_id}: Could not delete DAG. Response:\n{response.text}')


def delete_garbage_dags(garbage_dag_prefixes: tuple[str]) -> None:
    """Delete dags cloned from the original dags by users' requests"""

    # get all dags' info in airflow
    response = get_data(f'http://{AIRFLOW_API_URL}/api/v1/dags')
    for resp_dag in response["dags"]:
        dag_id = resp_dag["dag_id"]
        logger.info(f'{dag_id}: Found DAG')

        dag_in_dags_to_delete = any(dag_id.startswith(prefix) for prefix in garbage_dag_prefixes)
        latest_dag_run_state = get_data(
            f'http://{AIRFLOW_API_URL}/api/v1/dags/{dag_id}/dagRuns?order_by=-execution_date&limit=1'
        )["dag_runs"][0]["state"]

        # check if dag_id in garbage_dag_prefixes tuple and latest run was successful
        if dag_in_dags_to_delete and latest_dag_run_state == 'success':
            logger.info(f'{dag_id}: Found garbage prefix & successful latest run')
            delete_dag_data(dag_id)


with DAG(dag_id='garbage_handler_dag',
         default_args=args,
         schedule_interval='0 4 * * *',
         catchup=False) as dag:

    t1 = EmptyOperator(
        task_id='start_task'
    )
    t2 = PythonOperator(
        task_id=f'delete_garbage_dags',
        python_callable=delete_garbage_dags,
        op_kwargs={
            'garbage_dag_prefixes': GARBAGE_DAG_PREFIXES,
        }
    )
    t3 = EmptyOperator(
        task_id='end_task'
    )

    t1 >> t2 >> t3
