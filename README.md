# Recipe API: Docker Compose Demo

FastAPI + PostgreSQL demo for the Cloud Computing course (Docker Compose session).

## No working `docker-compose.yml`? On purpose.

This repository deliberately ships **without** a working `docker-compose.yml`. You write it yourself in the lab, from the slides. Everything else is here:

- `api/`: the Recipe API (FastAPI + SQLModel) and its `Dockerfile`
- `db/init.sql`: seeds a few recipes when PostgreSQL starts with an empty volume
- `debug/`: four **broken** Compose setups for the detective round, see `debug/README.md`

## Run (once your `docker-compose.yml` exists)

```bash
docker compose up -d
```

Open `http://localhost:8000/docs` to explore the API.

## Cleanup

```bash
docker compose down -v   # also removes the database volume
```
