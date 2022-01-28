# Python
from operator import gt, le
from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel, Field  # to create models ,schemas for data

# FastAPI
from fastapi import FastAPI, Body, Path, Query

app = FastAPI()

# Models (schemas)
# enum for the sizes of the pizza


class Size(Enum):
    big = "Familiar"
    medium = "Mediana"
    litle = "Personal"


class City(Enum):
    guayaquil = "Guayaquil"
    duran = "Duran"


class Pizza(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=40
    )
    price: int = Field(
        ...,
        gt=5,
        le=20
    )
    ingridients: str = Field(
        ...,
        min_length=1,
        max_length=200
    )
    size: Size = Field(default=Size.big)

    promotion: Optional[bool] = Field(default=False)


class Location(BaseModel):
    city: City = Field(default=City.guayaquil)
    country: str


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


# validations :  Request Body

@app.put('/pizza/{pizza_id}')
def update_pizza(
    pizza_id: int = Path(
        ...,
        gt=0,
        title='Pizza id',
        description="pizza id"
    ),
    pizza: Pizza = Body(...),
    location: Location = Body(...)

):
    result = pizza.dict()
    result.update(location.dict())
    result.update({"pizza_id": pizza_id})
    return result

# validations : Models
