import os
from pathlib import Path

import dags
import pytest
from airflow.models import DagBag

DAG_DIR: Path = Path(os.path.dirname(dags.__file__))


@pytest.fixture(scope="session")
def dag_bag():
    dag_bag = DagBag(
        dag_folder=str(DAG_DIR),
        include_examples=False,
    )
    return dag_bag
