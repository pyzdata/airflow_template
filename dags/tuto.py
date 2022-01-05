"""
Code that goes along with the Airflow located at:
http://airflow.readthedocs.org/en/latest/tutorial.html
"""
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from src.template import test_template

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2015, 6, 1),
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

with DAG("tutorial",
         default_args=default_args,
         schedule_interval=timedelta(1)
         ) as dag:
    # t1, t2 and t3 are examples of tasks created by instantiating operators
    t1 = BashOperator(task_id="print_date", bash_command="date", dag=dag)

    t2 = BashOperator(task_id="sleep", bash_command="sleep 5", retries=3, dag=dag)

    templated_command = """
        {% for i in range(5) %}
            echo "{{ ds }}"
            echo "{{ macros.ds_add(ds, 7)}}"
            echo "{{ params.my_param }}"
        {% endfor %}
    """

    t3 = BashOperator(
        task_id="templated",
        bash_command=templated_command,
        params={"my_param": "Parameter I passed in"},
    )
    t4 = PythonOperator(
        task_id="python_example",
        python_callable=test_template,
        op_kwargs={'example_var': 'some_value'}
    )

    t2.set_upstream(t1)
    t3.set_upstream(t1)
