# Customer Accounts Microservice

![Build Status](https://github.com/<YOUR-GITHUB-USERNAME>/customer-accounts/actions/workflows/ci-build.yaml/badge.svg)

A Flask REST API for managing customer accounts, built as the DevOps capstone:
CRUD API, CI with GitHub Actions, Talisman/CORS security, Docker, Kubernetes and a Tekton CD pipeline.

> Replace `<YOUR-GITHUB-USERNAME>` in this badge (and in `tekton/pipelinerun.yaml`) with your GitHub username.
> The badge only turns green after the CI workflow has run successfully on GitHub.

## Endpoints

| Operation | Method | URL |
|---|---|---|
| Create | POST | `/accounts` |
| List | GET | `/accounts` |
| Read | GET | `/accounts/<id>` |
| Update | PUT | `/accounts/<id>` |
| Delete | DELETE | `/accounts/<id>` |
| Health | GET | `/health` |

## Run locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
flask --app wsgi run --port 5000
```

## Test and lint

```bash
nosetests
flake8 accounts
pylint accounts
```

Tests use `pynose`, a maintained fork of nose that provides the `nosetests` command on current Python versions.

## Try the API

```bash
curl -i -X POST localhost:5000/accounts -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com","address":"1 Main St","phone_number":"555-1234"}'
curl -i localhost:5000/accounts
curl -i localhost:5000/accounts/1
curl -i -X PUT localhost:5000/accounts/1 -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com","address":"2 Side St","phone_number":"555-1234"}'
curl -i -X DELETE localhost:5000/accounts/1
```

## Docker

```bash
docker build -t accounts:1 .
docker images accounts
docker run --rm -p 8080:8080 accounts:1
```

## Kubernetes

```bash
kubectl apply -f kubernetes/
kubectl get all -l app=accounts
```

## Tekton CD pipeline

```bash
kubectl apply -f tekton/pvc.yaml -f tekton/tasks.yaml -f tekton/pipeline.yaml
kubectl create -f tekton/pipelinerun.yaml
tkn pipelinerun logs --last
```

The pipeline references the `git-clone`, `buildah` and `openshift-client` tasks from Tekton Hub/ClusterTasks,
which the lab environment provides. Install them first if your cluster lacks them.

## Layout

```
accounts/      application package (factory, models, routes)
tests/         unit tests
kubernetes/    deployment and service manifests
tekton/        CD pipeline definitions
docs/          user stories
```
