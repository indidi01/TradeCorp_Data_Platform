from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
from datetime import datetime, timedelta
import os

default_args = {
    "owner": "tradecorp",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

PROJECT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

MOUNTS = [
    Mount(
        source=os.path.join(PROJECT_DIR, "src"),
        target="/src",
        type="bind",
    ),
    Mount(
        source=os.path.join(PROJECT_DIR, "data"),
        target="/data",
        type="bind",
    ),
    Mount(
        source=os.path.join(PROJECT_DIR, ".env"),
        target="/.env",
        type="bind",
        read_only=True,
    ),
]

with DAG(
    dag_id="tradecorp_etl_pipeline",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule="0 6 * * *",
    catchup=False,
    tags=["tradecorp", "etl", "spark"],
) as dag:

    read_data = DockerOperator(
        task_id="read_data",
        image="tradecorp-spark",
        docker_url="unix://var/run/docker.sock"
        network_mode="tradecorp_default",
        auto_remove=True,
        Mount_tmp_dir=False,
        mounts=MOUNTS,
        command="spark-submit /home/jovyan/src/reader.py",
    ),

    clean_data = DockerOperator(
        task_id="clean_data",
        image="tradecorp-spark",
        docker_url="unix://var/run/docker.sock",
        network_mode="tradecorp_default",
        auto_remove=True,
        mounts=MOUNTS,
        command="spark-submit /home/jovyan/src/clean.py",
    ),

    transform_data = DockerOperator(
        task_id="transform_data",
        image="tradecorp-spark",
        docker_url="unix://var/run/docker.sock",
        network_mode="tradecorp_default",
        auto_remove=True,
        mounts=MOUNTS,
        command="spark-submit /home/jovyan/src/transformer.py",
    )

    read_data >> clean_data >> transform_data