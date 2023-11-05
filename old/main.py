import json
from typing import Union
from fastapi import FastAPI
import sqlite3
from entity.films import films
from entity.director import director
from entity.style import style
from pydantic import BaseModel
from typing import List
from flask import Flask

class Director(BaseModel):
    id: int | None = None
    director_first_name: str | None = None
    director_last_name: str | None = None
    director_is_awarded: bool | None = None
    director_birth_date: str | None = None

class Style(BaseModel):
    id: int | None = None
    style_name: str | None = None
    style_description: str | None = None

class Item(BaseModel):
    id: int
    films_title: str | None = None
    films_plot: str | None = None
    films_release_year: int | None = None
    films_release_date: str | None = None
    films_rating: int | None = None
    films_image_url: str | None = None
    films_running_time: int | None = None
    director: List[Director] | None = None
    style: List[Style] | None = None

flaskApp = Flask(__name__)
app = FastAPI()


@flaskApp.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.get("/api/films") #Récupére la liste de tous les films
def read_root():
    entity = films()
    return entity.getAll()

@app.get("/api/films/{id}") #Récupère les détails d’un film précisé par :id
def read_item(id: int):
    entity = films()
    return entity.getById(id)

@app.get("/api/directeurs/{id}") #Récupère les détails d’un directeur précisé par :id
def read_item(id: int):
    entity = director()
    return entity.getById(id)

@app.get("/api/style") #Récupère la liste de tous les genres
def read_root():
    entity = style()
    return entity.getAll()

@app.post("/api/films") #Ajout d'un film
def read_item(item: Item):
    entity = films()
    return entity.postItem(item)

@app.post("/api/directeurs") #Ajout d’un directeur
def read_item(item_id: int):
    return {"item_id": item_id, "q": q}

@app.put("/api/films/{id}") #Modification du directeur précisé par :id
def read_item(item_id: int):
    return {"item_id": item_id, "q": q}

@app.put("/api/directeurs/{id}") #Modification du directeur précisé par :id
def read_item(item_id: int):
    return {"item_id": item_id, "q": q}

@app.put("/api/genre/{id}") #Modification du genre précisé par :id
def read_item(item_id: int):
    return {"item_id": item_id, "q": q}

@app.delete("/api/films/{id}") #Suppression du film précisé par :id
def read_item(item_id: int):
    return {"item_id": item_id, "q": q}

