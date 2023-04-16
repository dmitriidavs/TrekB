import datetime as dt

from airflow.models import DAG, Variable
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator


default_args = {
    'owner': 'dmitriidavs',
    'start_date': dt.datetime(2023, 4, 13, 10, 0, 0, 0),
    'retries': 2,
    'retry_delay': dt.timedelta(minutes=1),
    'depends_on_past': False,
}


def on_api_trigger(**context) -> None:
    custom_args = context['dag_run'].conf.get('test_base_dag_args')
    print('*' * 150)
    print(f'Task triggered with custom arguments: {custom_args} - {dt.datetime.now()}')
    print('*' * 150)


with DAG(dag_id='test_base_dag',
         default_args=default_args,
         schedule_interval='@once',
         catchup=False):
    t1 = EmptyOperator(
        task_id='start_task',
    )
    t2 = PythonOperator(
        task_id=f'triggered_on_api_call',
        python_callable=on_api_trigger,
        provide_context=True,
    )
    t3 = EmptyOperator(
        task_id='end_task',
    )

    t1 >> t2 >> t3
