# Sample Project - Airflow

Developing and Running Airflow DAGs locally.


## Setup
```shell
brew install helm
brew upgrade helm
```


## Usage

```shell
make up
make port-forward
# <ctrl+c> to exit port-forward
make down
```


## Development

```shell
helm repo add apache-airflow https://airflow.apache.org

make update-chart-dependencies
make lint
```


# References
* [Extending Airflow's Helm Chart](https://airflow.apache.org/docs/helm-chart/stable/extending-the-chart.html)


# TODO
* [x] create helm chart wrapper around airflow+namespace
* [x] set desired default airflow values
* [ ] avoid needing to port-forward
* [x] add pvc for dags to chart (https://airflow.apache.org/docs/helm-chart/stable/manage-dag-files.html#mounting-dags-from-an-externally-populated-pvc)
* [x] add sample dag (with PythonOperators)
* [x] add sample dag (with PodOperators)
* [ ] update helm chart to allow multiple mounted dag folders
