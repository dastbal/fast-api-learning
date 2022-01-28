# Python
from typing import Optional

# Pydantic
from pydantic import BaseModel  # to create models ,schemas for data

# FastAPI
from fastapi import FastAPI, Path, Query
from fastapi import Body

app = FastAPI()

# Models (schemas)


class Pizza(BaseModel):
    title: str
    price: int
    ingridients: list
    description:  str
    promotion: Optional[bool] = False


@app.get('/')
def home():
    return {
        "title": "hello word"
    }

# Request and responde Body


@app.post('/pizza/new')
def create_pizza(pizza: Pizza = Body(...)):
    return pizza

# validations query


@app.get('/pizza/detail')
def show_pizza(
    title: Optional[str] = Query(
        None,
        min_length=1,
        max_length=30,
        title='Pizza title',
        description="pizza tile information needs to have 1 and 50 characters"
    )
):
    return {

        "title": title
    }

# validations path parameters


@app.get('/pizza/detail/{pizza_id}')
def show_pizza(
    pizza_id: int = Path(
        ...,
        gt=0,
        title='Pizza id',
        description="pizza id"
    )
):
    return {

        pizza_id: "Found"
    }
