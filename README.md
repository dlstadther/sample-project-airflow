# Sample Project - Airflow

Developing and Running Airflow DAGs locally.


## Setup
```shell
brew tap little-angry-clouds/homebrew-my-brews
brew install helmenv
brew upgrade helmenv

helmenv install 3.17.3

brew install kubernetes-cli
brew upgrade kubernetes-cli
```

Additionally, configure a local kubernetes cluster. A simple example requires:
1. Install Docker Desktop
2. Settings -> Kubernetes -> Enable Kubernetes -> Kubeadm -> Apply & Restart
3. `kubectl config use-context docker-desktop`


## Usage

```shell
make k8s-install
# http://localhost
# user/pass defaults to `admin/admin` (or whatever user is set in values.yaml's `airflow.webserver.defaultUser`)

# if you have a conflict on localhost port 80, then you can port-forward 8080 with:
# make port-forward
# <ctrl+c> to exit port-forward

make k8s-uninstall
```


## Development

```shell
helm repo add apache-airflow https://airflow.apache.org
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

make k8s-update-chart-dependencies
make k8s-lint

make init
make install
make format
make lint
make test
```


# References
* [Extending Airflow's Helm Chart](https://airflow.apache.org/docs/helm-chart/stable/extending-the-chart.html)


# TODO
* [x] fix helm deployment (wait for db migration to finish; but k8s job never launched)
* [ ] support for packaged dags
* [ ] pv hostpath vs `kubectl cp` to dag folder
* [x] airflow 3.x
