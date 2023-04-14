import os
import logging
import datetime as dt

import requests
from requests.exceptions import HTTPError
from airflow.models import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.exceptions import AirflowException

from includes.creds import *


args = {
    'owner': 'admin',
    'start_date': dt.datetime(2023, 4, 13, 10, 0, 0, 0),
    'retries': 2,
    'retry_delay': dt.timedelta(minutes=3),
    'depends_on_past': False,
}

logging.basicConfig(
    format='[%(levelname)s] %(name)s: %(message)s - %(asctime)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logging.getLogger(name='lambda').setLevel(logging.INFO)


def delete_dag(dag_name: str, dag_file_path: str) -> bool:
    """Delete dag"""

    # send delete request to Airflow API
    url = f'{AIRFLOW_API_URL}/{dag_name}'
    response = requests.delete(url,
                               auth=AIRFLOW_API_AUTH,
                               headers=AIRFLOW_API_HEADERS)

    # check response for successful deletion
    if response.status_code != 204:
        logging.info(f'Could not delete DAG {dag_name}: {response.text}')
        return False

    # delete file by its path
    if not os.path.exists(dag_file_path):
        logging.info(f'Could not find DAG {dag_name}: {dag_file_path}')
        return False
    else:
        os.remove(dag_file_path)
        logging.info(f'DAG {dag_name} deleted successfully')
        return True


def delete_garbage_dags(dags_to_delete: tuple[tuple[str, str]], dags_folder_path: str) -> None:
    """Delete dags cloned from the original dags by users"""

    for dag_name, dag_file_name in dags_to_delete:
        # check that dag finished execution - TODO: dag_name as wildcard (dag_name + user_id)
        last_dag_runs_url = f'{AIRFLOW_API_URL}/{dag_name}/dagRuns?order_by=-execution_date&state=success'
        response = requests.get(last_dag_runs_url,
                                auth=AIRFLOW_API_AUTH,
                                headers=AIRFLOW_API_HEADERS)
        if response.status_code != 200:
            raise AirflowException(f'Could not retrieve DAGs: {response.text}')

        last_dag_runs = response.json()

        print(last_dag_runs)

        # # get dag file path
        # dag_file_path = os.path.join(dags_folder_path, dag_file_name)
        #
        # # delete dag
        # delete_dag(dag_name, dag_file_path)


with DAG(dag_id='garbage_handler_dag',
         default_args=args,
         schedule_interval='@hourly',
         catchup=False) as dag:
    t1 = EmptyOperator(
        task_id='start_task'
    )
    t2 = PythonOperator(
        task_id=f'delete_garbage_dags',
        python_callable=delete_garbage_dags,
        op_kwargs={
            'dags_to_delete': DAGS_TO_DELETE,
            'dags_folder': DAGS_FOLDER_PATH
        }
    )
    t3 = EmptyOperator(
        task_id='end_task'
    )

    t1 >> t2 >> t3
