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

### Quick Deploy (using script)

```bash
chmod +x deploy-kind.sh
./deploy-kind.sh
```

### Manual Deploy

### 1. Create kind cluster

```bash
kind create cluster --name demo-cluster
```

### 2. Load image into kind

```bash
docker build -t username/ccDemo:latest .
kind load docker-image username/ccDemo:latest --name demo-cluster
```

### 3. Create namespace

```bash
kubectl create namespace streamlit-demo
```

### 4. Deploy Redis

Create `redis-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
  namespace: streamlit-demo
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis:7-alpine
        ports:
        - containerPort: 6379
---
apiVersion: v1
kind: Service
metadata:
  name: redis
  namespace: streamlit-demo
spec:
  selector:
    app: redis
  ports:
  - port: 6379
    targetPort: 6379
```

Apply:
```bash
kubectl apply -f redis-deployment.yaml
```

### 5. Deploy Streamlit

Create `streamlit-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: streamlit
  namespace: streamlit-demo
spec:
  replicas: 2
  selector:
    matchLabels:
      app: streamlit
  template:
    metadata:
      labels:
        app: streamlit
    spec:
      containers:
      - name: streamlit
        image: username/ccDemo:latest
        imagePullPolicy: Never
        ports:
        - containerPort: 8501
        env:
        - name: REDIS_HOST
          value: "redis"
        - name: REDIS_PORT
          value: "6379"
---
apiVersion: v1
kind: Service
metadata:
  name: streamlit
  namespace: streamlit-demo
spec:
  type: NodePort
  selector:
    app: streamlit
  ports:
  - port: 8501
    targetPort: 8501
    nodePort: 30000
```

Apply:
```bash
kubectl apply -f streamlit-deployment.yaml
```

### 6. Access the application

```bash
kubectl port-forward -n streamlit-demo service/streamlit 8501:8501
```

Open browser to `http://localhost:8501`

### 7. Verify deployment

```bash
kubectl get all -n streamlit-demo
kubectl logs -n streamlit-demo deployment/streamlit
kubectl logs -n streamlit-demo deployment/redis
```

### 8. Scale the application

```bash
kubectl scale deployment/streamlit --replicas=3 -n streamlit-demo
kubectl get pods -n streamlit-demo -w
```

### 9. Cleanup

```bash
kubectl delete namespace streamlit-demo
kind delete cluster --name demo-cluster
```