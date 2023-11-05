from fastapi import FastAPI
from entity.FIlms import Films, FilmModel
from entity.Director import Director, DirectorModel
from entity.Style import Style

app = FastAPI()

@app.get("/api/films") #Récupére la liste de tous les films
def read_item():
    filmClass = Films()
    response, responseStatus = filmClass.getAll()
    return {"Status": responseStatus, "Response": response}

@app.get("/api/films/{id}") #Récupère les détails d’un film précisé par :id
def read_item(id: int):
    filmClass = Films()
    response, responseStatus = filmClass.getBy("id", id)
    return {"Status": responseStatus, "Response": response}

@app.get("/api/directeurs/{id}") #Récupère les détails d’un directeur précisé par :id
def read_item(id: int):
    directorClass = Director()
    response, responseStatus = directorClass.getBy("id", id)
    return {"Status": responseStatus, "Response": response}

@app.get("/api/style") #Récupère la liste de tous les genres
def read_item():
    styleClass = Style()
    response, responseStatus = styleClass.getAll()
    return {"Status": responseStatus, "Response": response}

@app.post("/api/films") #Ajout d'un film
def read_item(filmData: FilmModel):
    filmClass = Films()
    response, responseStatus = filmClass.add(filmData)
    return {"Status": responseStatus, "Response": response}

@app.post("/api/directeurs") #Ajout d’un directeur
def read_item(directorData: DirectorModel):
    directorClass = Director()
    response, responseStatus = directorClass.add(directorData)
    return {"Status": responseStatus, "Response": response}

@app.put("/api/films") #Modification du film
def read_item():
    return {"Status": "responseStatus", "Response": "response"}

@app.put("/api/directeurs") #Modification du directeur précisé par :id
def read_item():
    return {"Status": "responseStatus", "Response": "response"}

@app.put("/api/style") #Modification du genre précisé par :id
def read_item():
    return {"Status": "responseStatus", "Response": "response"}

@app.delete("/api/films/{id}") #Suppression du film précisé par :id
def read_item():
    return {"Status": "responseStatus", "Response": "response"}