import logging
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

logger = logging.getLogger(__name__)

PROJECT = "/opt/airflow/project"
VENV = "/home/airflow/pipeline_venv/bin"


def notify_failure(context):
    ti = context["task_instance"]
    logger.error(
        "Task %s in DAG %s failed on try %s",
        ti.task_id,
        ti.dag_id,
        ti.try_number,
    )


default_args = {
    "owner": "data-engineering",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "on_failure_callback": notify_failure,
}

with DAG(
    dag_id="air_quality_pipeline",
    description="Ingest -> load -> dbt for Indian city air quality data",
    start_date=datetime(2026, 11, 1),
    schedule="@daily",
    catchup=False,
    default_args=default_args,
    tags=["portfolio", "air-quality"],
) as dag:

    ingest_raw = BashOperator(
        task_id="ingest_raw",
        bash_command=f"cd {PROJECT} && {VENV}/python ingestion/ingest.py",
    )

    load_raw = BashOperator(
        task_id="load_raw",
        bash_command=f"cd {PROJECT} && {VENV}/python load/load_raw.py",
    )

    dbt_seed = BashOperator(
        task_id="dbt_seed",
        bash_command=f"cd {PROJECT}/transform && {VENV}/dbt seed --profiles-dir .",
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"cd {PROJECT}/transform && {VENV}/dbt run --profiles-dir .",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"cd {PROJECT}/transform && {VENV}/dbt test --profiles-dir .",
    )

    ingest_raw >> load_raw >> dbt_seed >> dbt_run >> dbt_test