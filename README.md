# Recipe API: Docker Compose Demo

FastAPI + PostgreSQL demo for the Cloud Computing course (Docker Compose session).

## The `docker-compose.yml` is broken. On purpose.

It contains **three bugs**. Your job in the lab: make it run.

```bash
docker compose up -d --build
curl http://localhost:8000/recipes   # goal: returns a list of recipes
```

Tools: `docker compose ps`, `docker compose logs api`, `docker compose config`.

One bug hides once the database volume exists. Final check:

```bash
docker compose down -v && docker compose up -d
```

The fixed version is on the slides.

## What is here

- `api/`: the Recipe API (FastAPI + SQLModel) and its `Dockerfile`
- `db/init.sql`: seeds a few recipes when PostgreSQL starts with an empty volume
- `config/.env`: database credentials (demo values)

## Cleanup

```bash
docker compose down -v   # also removes the database volume
```
