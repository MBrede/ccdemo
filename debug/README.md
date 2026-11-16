# Detective Round: Broken Compose Files

Each folder holds a Compose setup that does not work. Find out **why**, then fix it.

```bash
cd debug/01
docker compose up -d --build
```

Tools: `docker compose ps`, `docker compose logs <service>`, `docker compose config`.

Clean up before the next case (all cases use port 8000):

```bash
docker compose down -v
```

**Case 02** needs two steps: start it once and check that `http://localhost:8000/recipes` works. Then change `POSTGRES_PASSWORD` in `.env` and run `docker compose up -d` again.
