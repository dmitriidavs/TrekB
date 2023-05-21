import datetime as dt

from airflow.models import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.operators.telegram_operator import TelegramOperator
from moralis import evm_api

from includes.CustomConnectors.DBMSconnection import DBMSCreateConnection
from includes.CustomConnectors.context import ContextOperator
from includes.utils.log import logger
from includes.utils.notification import notify_on_task_failure
from includes.creds import *


args = {
    'owner': 'dmitriidavs',
    'start_date': dt.datetime(2023, 5, 3, 10, 0, 0, 0),
    'retries': 2,
    'retry_delay': dt.timedelta(seconds=3),
    'depends_on_past': False,
    'on_failure_callback': notify_on_task_failure
}


def get_wallet_balance(address: str, **context) -> None:
    pass


def apply_changes_in_portfolio() -> None:
    pass


with DAG(dag_id='import_wallet_balance_dag',
         default_args=args,
         schedule_interval='@once',
         catchup=False) as dag:

    t_start = EmptyOperator(
        task_id='start_task'
    )
    t_get_wallet_balance = PythonOperator(
        task_id=f'get_wallet_balance',
        python_callable=get_wallet_balance,
        op_kwargs={
            'address': 'passed_by_api',
        }
    )
    t_send_ok_message = TelegramOperator(
        task_id="send_ok_message_telegram",
        telegram_conn_id=BOT_API_TOKEN,
        chat_id=CHAT_ID,
        text="Hello from Airflow!"
    )
    t_end = EmptyOperator(
        task_id='end_task'
    )

    t_start >> t_get_wallet_balance >> t_send_ok_message >> t_end
