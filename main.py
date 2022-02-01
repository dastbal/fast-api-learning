# Python
from typing import Optional
from enum import Enum

# Pydantic
# to create models ,schemas for data
from pydantic import BaseModel, EmailStr, Field

# FastAPI
from fastapi import Cookie, HTTPException, FastAPI, Body, File, Header, Path, Query, UploadFile, status, Form

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


class PizzBase(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=40
    )
    price: int = Field(
        ...,
        gt=5,
        le=20,
        example=10
    )
    ingridients: str = Field(
        ...,
        min_length=1,
        max_length=200
    )
    size: Size = Field(default=Size.big)

    promotion: Optional[bool] = Field(default=False)


class PizzaOut(PizzBase):
    pass


class Pizza(PizzBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=20,
        example='davidsteven'
    )


class Location(BaseModel):
    city: City = Field(default=City.guayaquil)
    country: str

    class Config:
        schema_extra = {
            "example": {
                "city": "Guayaquil",
                "country": "Ecuador",

            }
        }


class LoginOut(BaseModel):
    userName: str = Field(..., max_length=20, example='carli657')
    message: str = Field(default='Login Succesfully')


@app.get(
    path='/',
    status_code=status.HTTP_200_OK
)
def home():
    return {
        "title": "hello word"
    }
# Request and responde Body


@app.post(
    path='/pizza/new',
    tags=["pizzas"],
    status_code=status.HTTP_201_CREATED,
    response_model=PizzaOut)
def create_pizza(pizza: Pizza = Body(...)):
    return pizza
# validations query


@app.get(
    path='/pizza/detail',
    tags=["pizzas"],
    status_code=status.HTTP_200_OK
)
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


pizzas = [1, 2, 3, 4, 5, 6]


@app.get(
    path='/pizza/detail/{pizza_id}',
    tags=["pizzas"],
    status_code=status.HTTP_200_OK
)
def show_pizza(
    pizza_id: int = Path(
        ...,
        gt=0,
        title='Pizza id',
        description="pizza id"
    )
):
    # solving the error when the dara does not exist
    if pizza_id not in pizzas:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='this pizza does not exist'
        )
    return {

        pizza_id: "Found"
    }

# validations :  Request Body


@app.put(
    path='/pizza/{pizza_id}',
    tags=["pizzas"],
    status_code=status.HTTP_202_ACCEPTED
)
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


@app.post(
    path='/login',
    response_model=LoginOut,
    status_code=status.HTTP_200_OK


)
def login(userName: str = Form(...), password: str = Form(...)):
    return LoginOut(userName=userName)


# cookies and headers parameters

@app.post(
    path='/contact',
    status_code=status.HTTP_200_OK

)
def contact(
    firstName: str = Form(
        ...,
        min_length=3,
        max_length=20
    ),
    lasttName: str = Form(
        ...,
        min_length=3,
        max_length=20
    ),
    email:  EmailStr = Form(...),
    message: str = Form(
        ...,
        min_length=20,
        max_length=400
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
):
    return user_agent

# files


@app.post(
    path='/post-image',
    status_code=status.HTTP_202_ACCEPTED
)
def post_image(
    image: UploadFile = File(...)
):
    return {
        "Filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read())/1024, ndigits=2)
    }
