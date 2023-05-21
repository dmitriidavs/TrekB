import datetime as dt

import matplotlib
from airflow.models import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

from includes.utils.log import logger
from includes.utils.notification import notify_on_task_failure
from includes.creds import *


args = {
    'owner': 'dmitriidavs',
    'start_date': dt.datetime(2023, 5, 21, 10, 0, 0, 0),
    'retries': 2,
    'retry_delay': dt.timedelta(seconds=3),
    'depends_on_past': False,
    'on_failure_callback': notify_on_task_failure
}