#Python
from typing import Optional

#Pydantic
from pydantic import BaseModel # to create models ,schemas for data

#FastAPI
from fastapi import FastAPI
from fastapi import Body

app = FastAPI()

#Models (schemas)

class Pizza(BaseModel):
    title : str
    price: int
    ingridients : list
    description:  str
    promotion : Optional[bool] = False



@app.get('/')
def home():
    return {
        "title":"hello word"
    }

# Request and responde Body

@app.post('/pizza/new')
def create_pizza(pizza : Pizza = Body(...)):
    return pizza

