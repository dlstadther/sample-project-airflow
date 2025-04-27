CHART_PATH := ./k8s/local
NAMESPACE := airflow
RELEASE_NAME := local-airflow

k8s-create-namespace:
	@echo "Creating namespace $(NAMESPACE) if it doesn't exist"
	kubectl create namespace $(NAMESPACE) --dry-run=client -o yaml | kubectl apply -f -

k8s-delete-namespace:
	@echo "Deleting namespace $(NAMESPACE) even if it doesn't exist"
	kubectl delete namespace $(NAMESPACE)

k8s-install: k8s-create-namespace
	@echo "Installing $(RELEASE_NAME) in $(NAMESPACE) namespace"
	helm upgrade \
		$(RELEASE_NAME) \
		$(CHART_PATH) \
		--atomic \
		--install \
		--namespace=$(NAMESPACE) \
		--set localDags.pathToDags="$(PWD)/dags" \
		--timeout=10m \
		--values=$(CHART_PATH)/values.yaml

k8s-lint:
	@echo "Linting $(CHART_PATH)"
	helm lint $(CHART_PATH) \
		--values $(CHART_PATH)/values_2.yaml

k8s-port-forward:
	@echo "Port forwarding to $(RELEASE_NAME) in $(NAMESPACE) namespace"
	kubectl port-forward --namespace=$(NAMESPACE) svc/$(RELEASE_NAME)-webserver 8080:8080

k8s-uninstall:
	@echo "Uninstalling $(RELEASE_NAME) from $(NAMESPACE) namespace"
	helm uninstall \
		$(RELEASE_NAME) \
		--namespace=$(NAMESPACE)

k8s-update-chart-dependencies:
	@echo "Updating chart dependencies for $(CHART_PATH)"
	helm dependency update $(CHART_PATH)
	helm dependency build $(CHART_PATH)

format:
	@echo "Formatting Python code"
	uv run ruff format

init:
	@echo "Initializing environment"
	curl -LsSf https://astral.sh/uv/install.sh | sh
	uv self update

install:
	@echo "Installing dependencies"
	uv sync

lint:
	@echo "Linting Python code"
	uv run ruff check --fix

test:
	@echo "Running tests"
	uv run pytest -vv
	uv run coverage report
