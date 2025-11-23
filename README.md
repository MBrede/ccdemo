# Container Orchestration Demo (ccDemo)

Streamlit application demonstrating container orchestration with Redis caching.

## Features

- Page view counter using Redis
- Interactive message caching
- Real-time Redis statistics
- Container health monitoring


## Run with Docker Compose

```bash
docker compose up -d
```

## Environment Variables

- `REDIS_HOST`: Redis server hostname (default: redis)
- `REDIS_PORT`: Redis server port (default: 6379)

## Access

Open browser to `http://localhost:8501`

## Deploy to Kubernetes (kind)

### 1. Create kind cluster

```bash
kind create cluster --name demo-cluster
```

or for more nodes:

```bash
kind create cluster --name demo-cluster --config kind-config.yaml
```

### 2. Create namespace

```bash
kubectl create namespace streamlit-demo
```

### 3. Apply all manifests

```bash
kubectl apply -f k8s/redis-deployment.yaml 
kubectl apply -f k8s/redis-service.yaml 
kubectl apply -f k8s/streamlit-deployment.yaml 
kubectl apply -f k8s/streamlit-service.yaml 

kubectl get all -n streamlit-demo

kubectl get pods -n streamlit-demo -w
```



### 4. Access the application

Open browser to `http://localhost:8501`

### 5. Verify deployment

```bash
kubectl get all -n streamlit-demo
kubectl logs -n streamlit-demo deployment/streamlit
kubectl logs -n streamlit-demo deployment/redis
```

### 6. Scale the application

```bash
kubectl scale deployment/streamlit --replicas=3 -n streamlit-demo
kubectl get pods -n streamlit-demo -w
```

### 7. Cleanup

```bash
kubectl delete namespace streamlit-demo
kind delete cluster --name demo-cluster
```