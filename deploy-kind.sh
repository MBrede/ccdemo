#!/bin/bash

set -e

echo "Deploying ccdemo to kind..."

echo "Creating kind cluster..."
kind create cluster --name demo-cluster 2>/dev/null || echo "Cluster already exists"

echo "Loading image into kind..."
kind load docker-image mbrede/ccdemo:latest --name demo-cluster

echo " Creating namespace..."
kubectl create namespace streamlit-demo 2>/dev/null || echo "Namespace already exists"

echo " Deploying Redis..."
kubectl apply -f k8s/redis-deployment.yaml

echo "Deploying Streamlit..."
kubectl apply -f k8s/streamlit-deployment.yaml

echo "Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app=redis -n streamlit-demo --timeout=60s
kubectl wait --for=condition=ready pod -l app=streamlit -n streamlit-demo --timeout=60s

echo "Deployment complete!"
echo ""
echo "Check status:"
echo "  kubectl get all -n streamlit-demo"
echo ""
echo "Access application:"
echo "  kubectl port-forward -n streamlit-demo service/streamlit 8501:8501"
echo "  Then open: http://localhost:8501"
echo ""
echo "Cleanup:"
echo "  kubectl delete namespace streamlit-demo"
echo "  kind delete cluster --name demo-cluster"