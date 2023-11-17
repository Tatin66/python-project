from fastapi import FastAPI
from entity.FIlms import Films, FilmModel
from entity.Director import Director, DirectorModel
from entity.Style import Style, StyleModel

app = FastAPI()

@app.get("/api/films") #Récupére la liste de tous les films
def read_item():
    filmClass = Films()
    response = filmClass.getAll()
    return response

@app.get("/api/films/{id}") #Récupère les détails d’un film précisé par :id
def read_item(id: int):
    filmClass = Films()
    response = filmClass.getBy("id", id)
    return response

@app.get("/api/directeurs/{id}") #Récupère les détails d’un directeur précisé par :id
def read_item(id: int):
    directorClass = Director()
    response = directorClass.getBy("id", id)
    return response

@app.get("/api/style") #Récupère la liste de tous les genres
def read_item():
    styleClass = Style()
    response = styleClass.getAll()
    return response

@app.get("/api/style/{id}") #Récupère la liste de tous les genres
def read_item(id: int):
    styleClass = Style()
    response = styleClass.getBy("id", id)
    return response

@app.post("/api/films") #Ajout d'un film
def read_item(filmData: FilmModel):
    filmClass = Films()
    response = filmClass.add(filmData)
    return response

@app.post("/api/directeurs") #Ajout d’un directeur
def read_item(directorData: DirectorModel):
    directorClass = Director()
    response = directorClass.add(directorData)
    return response

@app.put("/api/films") #Modification du film
def read_item(filmData: FilmModel):
    filmClass = Films()
    response = filmClass.modify(filmData)
    return response

@app.put("/api/directeurs") #Modification du directeur précisé par :id
def read_item(directorData: DirectorModel):
    directorClass = Director()
    response, responseStatus = directorClass.modify(directorData)
    return response

@app.put("/api/style") #Modification du genre précisé par :id
def read_item(directorStyle: StyleModel):
    styleClass = Style()
    response = styleClass.modify(directorStyle)
    return response

@app.delete("/api/films/{id}") #Suppression du film précisé par :id
def read_item(id: int):
    filmClass = Films()
    response = filmClass.delete(id)
    return response

@app.api_route("/{path_name:path}", methods=["GET"])
def catch_all():
    return "Bad Url"

@app.api_route("/{path_name:path}", methods=["POST"])
def catch_all():
    return "Bad Url"

@app.api_route("/{path_name:path}", methods=["PUT"])
def catch_all():
    return "Bad Url"

@app.api_route("/{path_name:path}", methods=["DELETE"])
def catch_all():
    return "Bad Url"