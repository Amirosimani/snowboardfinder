from airflow import DAG
from airflow.operators.bash import BashOperator

from datetime import datetime, timedelta


# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}

with DAG(
    'snowboard_finder',
    default_args=default_args,
    description='Get snowboard ratings from the internet and calculate similarity',
    # schedule_interval=timedelta(days=1),
    start_date=datetime(2022, 1, 1),
    catchup=False,
    tags=['snowboard'],
) as dag:

    t1 = BashOperator(
        task_id='scraper',
        bash_command='/Users/amir/Documents/projects/snowboardfinder/src/web_scraper/src/scraper.py',
        params={"gender": "mens",
                "mode": "local"}
    )

    t2 = BashOperator(
        task_id='similarity',
        depends_on_past=True,
        bash_command='/Users/amir/Documents/projects/snowboardfinder/src/similarity/similarity.py',
        retries=3,
    )

    # t2 will depend on t1 running successfully to run.
    t1.set_downstream(t2)
