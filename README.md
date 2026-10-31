# K8s Store Factory

A small platform where a user clicks **Launch Store** and gets their own isolated WordPress + MySQL store running on Kubernetes. Clicking **Delete** removes the store and everything inside it.

A Flask backend talks to the Kubernetes API through the Python client. Every store lives in its own namespace, with its own database, storage and generated passwords.

## How it works

```
Browser (dashboard)
   |  Launch Store / Delete
   v
Flask API  --->  SQLite (users, stores, status)
   |
   |  Python kubernetes client
   v
Kubernetes (kind cluster)
   namespace: store-<id>
     |-- Secret      (random MySQL passwords)
     |-- PVC         (MySQL data, size chosen by the user)
     |-- MySQL       Deployment + Service
     |-- WordPress   Deployment + Service + PVC
```

**Launch**
1. The dashboard sends the request with a token. The backend validates the store id and storage size.
2. A row is saved in SQLite with status `provisioning`.
3. A background thread creates the namespace `store-<id>` and applies `k8s/store.yaml`. The MySQL passwords are random for every store.
4. The thread checks that the MySQL and WordPress Deployments are ready, then sets the status to `ready` (or `failed`).
5. The dashboard refreshes by itself while a store is `provisioning`.

**Delete**
1. The backend looks up the store id, then deletes the namespace `store-<id>`.
2. Kubernetes removes everything inside it (Pods, Services, PVCs, Secret).
3. The store row is removed from SQLite.

## Tech stack

- Frontend: HTML, CSS, JavaScript, served by nginx
- Backend: Python, Flask, SQLite
- Kubernetes client: `kubernetes` (Python)
- Containers: Docker
- Local cluster: kind
- Store: WordPress 6 and MySQL 8

## Project layout

```
Backend part/
  app.py                       Flask app
  controller/                  API routes (users, stores)
  model/                       database access
  store_k8s.py                 create / delete / status of a store on Kubernetes
  database.py                  SQLite setup
Frontend part/                 dashboard, new store page, login
k8s/
  backend-deployment.yaml      backend manifests (earlier milestone)
  backend-service.yaml
  frontend.yaml                frontend Deployment + Service
  store.yaml                   template applied for every store
```

## Run it locally

Requirements: Docker Desktop, [kind](https://kind.sigs.k8s.io/), kubectl, Python 3.

```bash
# 1. cluster
kind create cluster --name store-factory

# 2. frontend image into the cluster
docker build -t store-frontend "Frontend part"
kind load docker-image store-frontend --name store-factory
kubectl apply -f k8s/frontend.yaml

# 3. open the dashboard (keep this running)
kubectl port-forward svc/frontend 8080:80

# 4. backend, in a second terminal
cd "Backend part"
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
python app.py
```

Open `http://localhost:8080`, sign up, log in and press **Launch Store**.

To open a store, use the command shown on its card, for example:

```bash
kubectl port-forward -n store-<id> svc/wordpress 8081:80
```

then open `http://localhost:8081`.

Useful checks:

```bash
kubectl get ns
kubectl get pods -n store-<id>
```

## Current limits

- Stores are opened with `kubectl port-forward`. There is no Ingress yet, so no public store URL.
- The Flask backend runs on the laptop and uses the local kubeconfig. Running it inside the cluster needs RBAC, which is not added yet.
- The passwords inside `k8s/store.yaml` are placeholders. Real stores get random passwords from `store_k8s.py`.
- The WordPress admin account is created on the WordPress install screen, not by the platform.
- The dashboard limits a user to 3 stores.

## Next steps

- Ingress with a hostname per store
- RBAC so the backend can run inside the cluster
- GitHub Actions to build and push the Docker images
- Helm chart for the store