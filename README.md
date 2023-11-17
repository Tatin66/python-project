installation du projet :
1. python -m venv .\venv (pour powershell) python -m venv venv (pour cmd)
2. .\venv\Scripts\activate (pour powershell) venv\Scripts\activate (pour cmd)
3. pip install -r requirements.txt
4. cd .\api\
5. uvicorn MainApi:app --host 127.0.0.1 --port 8000 

L'api : 
l'api est accessible via l'URL http://127.0.0.1:8000/

Les routes disponnibles sont :
- GET /api/films -- récupère la liste de tous les films
- GET /api/films/{id} -- Récupère les détails d’un film précisés par : id
- GET /api/directeurs/{id} -- Récupère les détails d’un directeur précisés par : id
- GET /api/style -- Récupère la liste de tous les genres
- POST /api/films -- Ajout d'un film
- POST /api/directeurs -- Ajout d’un directeur 
- PUT /api/films -- Modification du film
- PUT /api/directeurs -- Modification du directeur précisé par :id 
- PUT /api/style -- Modification du genre précisé par :id
- DELETE /api/films/{id} -- Supprime un film

Pour les méthodes POST et PUT la requête doit être accompagné d'un json représentant
l'élément que vous voulez affecter.

Voici la liste des objets films, directeurs et styles :

1. Directeur :
 {
    "director_first_name": "Nom",
    "director_last_name": "Prenom",
    "director_is_awarded" : bool,
    "director_birth_date" : "10/08/1998"
}

2. Style :
{
    "style_name": "StyleName"
    "style_description" : "Description"
}

3. films :
{
    "films_title": "hello world",
    "films_plot": "plot",
    "films_release_year": 2012,
    "films_release_date": "12",
    "films_rating": 1,
    "films_image_url": "url",
    "films_running_time": 7,
    "director": [
        liste directeur 
    ],
    "style": [
        liste de style
    ]
}