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
# http://localhost

# if you have a conflict on localhost port 80, then you can port-forward 8080 with:
# make port-forward
# <ctrl+c> to exit port-forward

make down
```


## Development

```shell
helm repo add apache-airflow https://airflow.apache.org
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

make update-chart-dependencies
make lint
```


# References
* [Extending Airflow's Helm Chart](https://airflow.apache.org/docs/helm-chart/stable/extending-the-chart.html)


# TODO
* [ ] support for packaged dags
* [ ] pv hostpath vs `kubectl cp` to dag folder
* [ ] airflow 3.x
