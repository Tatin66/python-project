import json
from typing import Union
from fastapi import FastAPI
import sqlite3
from entity.films import films


app = FastAPI()

@app.get("/api/films") #Récupére la liste de tous les films
def read_root():
    entity = films()
    return entity.getAll()

@app.get("/api/films/{id}") #Récupère les détails d’un film précisé par :id
def read_item(item_id: int):
    return {"item_id": item_id, "q": q}

@app.get("/api/directeurs/{id}") #Récupère les détails d’un directeur précisé par :id
def read_item(item_id: int):
    return {"item_id": item_id, "q": q}

@app.get("/api/genre") #Récupère la liste de tous les genres
def read_item(item_id: int):
    return {"item_id": item_id, "q": q}

@app.post("/api/films") #Ajout d'un film
def read_item(item_id: int):
    return {"item_id": item_id, "q": q}

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

