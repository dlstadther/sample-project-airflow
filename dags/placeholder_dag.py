import logging
import os
from datetime import timedelta
from typing import Any

import pendulum
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator, ShortCircuitOperator
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from airflow.providers.google.cloud.operators.kubernetes_engine import GKEStartPodOperator

from utils.functions import can_i_run

logger = logging.getLogger(__name__)

DAG_ID = "placeholder_dag"
ENVIRONMENT = os.getenv("ENVIRONMENT")


def conditional_pod(**context) -> Any | None:
    """PythonOperator execution of PodOperator"""
    logger.info(f"Conditional Pod: {ENVIRONMENT=}")
    match ENVIRONMENT:
        case "local":
            logger.info("Local Pod")
            operator = KubernetesPodOperator(
                task_id="kubernetes_task",
                name="kubernetes_task",
                namespace="airflow",
                image="python:3.8-slim",
                image_pull_policy="Always",
                cmds=["python", "-c"],
                arguments=["print('Hello from KubernetesPodOperator!')"],
                is_delete_operator_pod=True,
                in_cluster=True,
                get_logs=True,
            )
            return operator.execute(context=context)
        case ("dev" | "qa" | "staging" | "prod"):
            logger.info("Remote Pod")
            logger.warning(f"Cannot run pod when {ENVIRONMENT=}")
            # operator = GKEStartPodOperator()
            return
        case _:
            raise ValueError(f"Invalid execution: {ENVIRONMENT=}")


with DAG(
    catchup=False,
    dag_id=DAG_ID,
    default_args={
        "depends_on_past": False,
        "start_date": pendulum.today("UTC").add(days=-2),
        "execution_timeout": timedelta(minutes=15),
        "retries": 1,
        "retry_delay": timedelta(minutes=2),
    },
    max_active_runs=5,
    render_template_as_native_obj=True,
    schedule=None,
    tags=["sample"],
) as dag:
    e = EmptyOperator(task_id="empty_task")

    s = ShortCircuitOperator(
        task_id="short_circuit_task",
        python_callable=can_i_run,
    )

    p = PythonOperator(
        task_id="python_task",
        python_callable=lambda: logger.info("Hello from PythonOperator!"),
    )

    k = PythonOperator(
        task_id="kubernetes_task",
        python_callable=conditional_pod,
    )

    _ = e >> s >> p
    _ = e >> k
