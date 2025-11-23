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
