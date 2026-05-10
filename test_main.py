import pytest
import main as app_module
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine
from sqlmodel.pool import StaticPool
from main import app

CARBONARA = {
    "name": "Spaghetti Carbonara",
    "cuisine": "Italian",
    "preparation_time": 30,
    "is_vegetarian": False,
}
RATATOUILLE = {
    "name": "Ratatouille",
    "cuisine": "French",
    "preparation_time": 60,
    "is_vegetarian": True,
}
TACOS = {
    "name": "Tacos al Pastor",
    "cuisine": "Mexican",
    "preparation_time": 45,
    "is_vegetarian": False,
}


@pytest.fixture(name="client")
def client_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    app_module.engine = engine
    SQLModel.metadata.create_all(engine)
    client = TestClient(app)
    client.post("/recipes", json=CARBONARA)
    client.post("/recipes", json=RATATOUILLE)
    client.post("/recipes", json=TACOS)
    yield client
    SQLModel.metadata.drop_all(engine)


# ── GET /recipes ──────────────────────────────────────────────────────────────

def test_get_all_recipes_returns_200(client):
    assert client.get("/recipes").status_code == 200

def test_get_all_recipes_returns_list(client):
    r = client.get("/recipes")
    assert isinstance(r.json(), list)
    assert len(r.json()) == 3


# ── GET /recipes/{id} ─────────────────────────────────────────────────────────

def test_get_recipe_by_id_returns_200(client):
    recipe_id = client.get("/recipes").json()[0]["id"]
    assert client.get(f"/recipes/{recipe_id}").status_code == 200

def test_get_missing_recipe_returns_404(client):
    assert client.get("/recipes/999").status_code == 404


# ── GET /recipes?cuisine=&is_vegetarian= ─────────────────────────────────────

def test_filter_by_cuisine_returns_only_matching(client):
    r = client.get("/recipes?cuisine=Italian")
    assert r.status_code == 200
    assert r.json() and all(rec["cuisine"] == "Italian" for rec in r.json())

def test_filter_by_vegetarian_returns_only_matching(client):
    r = client.get("/recipes?is_vegetarian=true")
    assert r.status_code == 200
    assert r.json() and all(rec["is_vegetarian"] for rec in r.json())


# ── POST /recipes ─────────────────────────────────────────────────────────────

def test_create_recipe_returns_201_with_id(client):
    r = client.post("/recipes", json={
        "name": "Miso Soup", "cuisine": "Japanese", "preparation_time": 15,
    })
    assert r.status_code == 201
    assert r.json()["id"] is not None

def test_create_duplicate_name_returns_409(client):
    r = client.post("/recipes", json=CARBONARA)
    assert r.status_code == 409

def test_invalid_cuisine_returns_422(client):
    r = client.post("/recipes", json={**CARBONARA, "name": "Bratwurst", "cuisine": "German"})
    assert r.status_code == 422

def test_invalid_preparation_time_returns_422(client):
    r = client.post("/recipes", json={**CARBONARA, "name": "Instant", "preparation_time": 0})
    assert r.status_code == 422


# ── PUT /recipes/{id} ─────────────────────────────────────────────────────────

def test_put_replaces_recipe_and_returns_200(client):
    recipe_id = client.get("/recipes").json()[0]["id"]
    r = client.put(f"/recipes/{recipe_id}", json={
        "name": "Spaghetti Carbonara", "cuisine": "Italian", "preparation_time": 25,
    })
    assert r.status_code == 200
    assert r.json()["preparation_time"] == 25

def test_put_missing_recipe_returns_404(client):
    r = client.put("/recipes/999", json={
        "name": "Ghost", "cuisine": "Other", "preparation_time": 10,
    })
    assert r.status_code == 404


# ── DELETE /recipes/{id} ──────────────────────────────────────────────────────

def test_delete_recipe_returns_204(client):
    recipe_id = client.get("/recipes").json()[0]["id"]
    assert client.delete(f"/recipes/{recipe_id}").status_code == 204

def test_delete_removes_recipe(client):
    recipe_id = client.get("/recipes").json()[0]["id"]
    client.delete(f"/recipes/{recipe_id}")
    assert client.get(f"/recipes/{recipe_id}").status_code == 404

def test_delete_missing_recipe_returns_404(client):
    assert client.delete("/recipes/999").status_code == 404
