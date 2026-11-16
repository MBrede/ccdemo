import os
from typing import Annotated, Literal

import psycopg
from fastapi import FastAPI, Query
from psycopg.rows import class_row
from pydantic import BaseModel, Field

Cuisine = Literal["Italian", "French", "Japanese", "Mexican", "Other"]


class RecipeBase(BaseModel):
    name: str = Field(min_length=1)
    cuisine: Cuisine
    preparation_time: int = Field(gt=0)
    is_vegetarian: bool = False


class Recipe(RecipeBase):
    id: int


class RecipeCreate(RecipeBase):
    pass


def connect():
    # One connection per request; rows come back as Recipe objects.
    return psycopg.connect(os.environ["DATABASE_URL"], row_factory=class_row(Recipe))


app = FastAPI(
    title="Recipe API",
    description="Restaurant Recipe API with PostgreSQL",
)


@app.get("/recipes", response_model=list[Recipe])
def get_recipes(
    cuisine: Annotated[Cuisine | None, Query(description="Filter by cuisine")] = None,
):
    with connect() as conn:
        if cuisine:
            return conn.execute(
                "SELECT * FROM recipe WHERE cuisine = %s", (cuisine,)
            ).fetchall()
        return conn.execute("SELECT * FROM recipe").fetchall()


@app.post("/recipes", response_model=Recipe, status_code=201)
def create_recipe(recipe: RecipeCreate):
    with connect() as conn:
        return conn.execute(
            "INSERT INTO recipe (name, cuisine, preparation_time, is_vegetarian) "
            "VALUES (%(name)s, %(cuisine)s, %(preparation_time)s, %(is_vegetarian)s) "
            "RETURNING *",
            recipe.model_dump(),
        ).fetchone()
