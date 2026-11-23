FROM apache/airflow:2.10.5

COPY orchestration/requirements-pipeline.txt /tmp/requirements-pipeline.txt

RUN python -m venv /home/airflow/pipeline_venv \
    && /home/airflow/pipeline_venv/bin/pip install --no-cache-dir -r /tmp/requirements-pipeline.txt