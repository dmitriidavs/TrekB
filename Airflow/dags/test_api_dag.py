import datetime as dt

from airflow.models import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator


args = {
    'owner': 'admin',
    'start_date': dt.datetime(2023, 4, 13, 10, 0, 0, 0),
    'retries': 2,
    'retry_delay': dt.timedelta(minutes=1),
    'depends_on_past': False,
}


def on_api_trigger(task_id: int) -> None:
    print(f'Task id: {task_id} triggered - {dt.datetime.now()}')


with DAG(dag_id='og_test_api_dag',
         default_args=args,
         schedule_interval='@once',
         catchup=False):
    t1 = EmptyOperator(
        task_id='start_task'
    )
    t2 = PythonOperator(
        task_id=f'triggered_on_api_call',
        python_callable=on_api_trigger,
        op_kwargs={
            'task_id': 1
        }
    )
    t3 = EmptyOperator(
        task_id='end_task'
    )

    t1 >> t2 >> t3
