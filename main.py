from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlmodel import Field, SQLModel, Session, create_engine, select
from typing import Optional, Literal
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://user:password@db/recipes")
engine = create_engine(DATABASE_URL)

Cuisine = Literal["Italian", "French", "Japanese", "Mexican", "Other"]


class RecipeCreate(BaseModel):
    name: str = Field(min_length=1)
    cuisine: Cuisine
    preparation_time: int = Field(gt=0)
    is_vegetarian: bool = False


class Recipe(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    cuisine: str
    preparation_time: int
    is_vegetarian: bool = False


def get_session():
    with Session(engine) as session:
        yield session


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(
    title="Recipe API",
    description="Restaurant Recipe API with PostgreSQL",
    lifespan=lifespan,
)


@app.get("/recipes", response_model=list[Recipe])
def get_recipes(session: Session = Depends(get_session)):
    return session.exec(select(Recipe)).all()


@app.post("/recipes", response_model=Recipe, status_code=201)
def create_recipe(recipe: RecipeCreate, session: Session = Depends(get_session)):
    db_recipe = Recipe.model_validate(recipe)
    session.add(db_recipe)
    session.commit()
    session.refresh(db_recipe)
    return db_recipe
