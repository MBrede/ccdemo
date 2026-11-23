import os
from typing import Annotated, Literal
import psycopg
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

os.environ["DATABASE_URL"] = "postgresql://user:password123@localhost:5432/recipes"

def connect():
    return psycopg.connect("postgresql://user:password123@localhost:5432/recipes", 
                           row_factory=class_row(Recipe))

# @app.get("/recipes/{recipe_id}", response_model=Recipe)
# def get_recipe(recipe_id: int):
#     with connect() as conn:
#         recipe = conn.execute(
#             "SELECT * FROM recipe WHERE id = %s", (recipe_id,)
#         ).fetchone()
#     if recipe is None:
#         raise HTTPException(status_code=404, detail="Recipe not found")
#     return recipe

def optional_filters(cuisine, is_vegetarian):# Optional filters
    with connect() as conn:
        sql, params = "SELECT * FROM recipe WHERE TRUE", []
        if cuisine:
            sql += " AND cuisine = %s"
            params.append(cuisine)
        if is_vegetarian is not None:
            sql += " AND is_vegetarian = %s"
            params.append(is_vegetarian)
        # mogrify = the query exactly as psycopg sends it, params filled in safely
        print(psycopg.ClientCursor(conn).mogrify(sql, params))
        lines = conn.execute(sql, params).fetchall()
        return lines
    
optional_filters("Italian", True)


def optional_fstring_filters(cuisine, is_vegetarian):# Optional filters
    with connect() as conn:
        cuisine_filter = f" AND cuisine = '{cuisine}'"  # SQL strings need single quotes
        veg_filter = f" AND is_vegetarian = {str(is_vegetarian).lower()}"
        sql, params = f"SELECT * FROM recipe WHERE TRUE {cuisine_filter if cuisine else ''} {veg_filter if is_vegetarian is not None else ''}", []
        print(sql)
        lines = conn.execute(sql, params).fetchall()
        return lines
    
optional_fstring_filters("Italian", None)