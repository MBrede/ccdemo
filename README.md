# Recipe API — Docker Compose Demo

FastAPI + PostgreSQL demo for the Cloud Computing course (Docker Compose session).

Demonstrates multi-container orchestration with Docker Compose: the API container connects to a PostgreSQL database using Compose DNS, with a named volume for persistence.

## Run

```bash
docker compose up -d
```

Open `http://localhost:8000/docs` to explore the API.

On first start, PostgreSQL runs `db/init.sql` and seeds a few recipes. It only does this while the `db-data` volume is empty: `docker compose down -v` to reseed.

## Test persistence

```bash
# Add a recipe via /docs, then:
curl http://localhost:8000/recipes          # data in PostgreSQL
docker compose restart api
curl http://localhost:8000/recipes          # still there after restart
docker compose down && docker compose up -d
curl http://localhost:8000/recipes          # still there after full restart
```

## Smoke test

```bash
docker compose run --rm smoke-test   # one-off job, skipped by `up` (profile: test)
```

## Detective round

`debug/` holds four broken Compose setups. See `debug/README.md`.

## Cleanup

```bash
docker compose down -v   # also removes the database volume
```

## Run tests

The test suite covers the full CRUD API students implement in the exercise.
It uses SQLite in-memory so no running database is needed.

```bash
pip install pytest httpx
pytest test_main.py -v
```
