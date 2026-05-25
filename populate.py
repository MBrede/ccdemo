import os
from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select

DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(DATABASE_URL)


class Recipe(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    cuisine: str
    preparation_time: int
    is_vegetarian: bool = False


SQLModel.metadata.create_all(engine)

RECIPES = [
    Recipe(name="Pasta Carbonara", cuisine="Italian", preparation_time=25, is_vegetarian=False),
    Recipe(name="Margherita Pizza", cuisine="Italian", preparation_time=30, is_vegetarian=True),
    Recipe(name="Chicken Tikka Masala", cuisine="Other", preparation_time=45, is_vegetarian=False),
    Recipe(name="Vegetable Stir Fry", cuisine="Japanese", preparation_time=20, is_vegetarian=True),
    Recipe(name="Beef Tacos", cuisine="Mexican", preparation_time=30, is_vegetarian=False),
    Recipe(name="Ratatouille", cuisine="French", preparation_time=60, is_vegetarian=True),
]

with Session(engine) as session:
    existing = session.exec(select(Recipe)).first()
    if existing:
        print("Database already populated, skipping.")
    else:
        for recipe in RECIPES:
            session.add(recipe)
        session.commit()
        print(f"Inserted {len(RECIPES)} recipes.")
