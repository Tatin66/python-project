import json
from typing import List

from entity.Entity import Entity
from entity.Director import DirectorModel, Director
from entity.Style import StyleModel, Style
from pydantic import BaseModel
class Films(Entity):
    def __init__(self):
        model = FilmModel()
        super().__init__("films", model)

    def getAll(self):
        sqlStr = """
            SELECT
                f.id AS film_id,
                f.films_title AS film_title,
                f.films_plot AS film_plot,
                f.films_release_year AS film_release_year,
                f.films_release_date AS film_release_date,
                f.films_rating AS film_rating,
                f.films_image_url AS film_image_url,
                f.films_running_time AS film_running_time,
                GROUP_CONCAT(DISTINCT d.id) AS director_id,
                GROUP_CONCAT(DISTINCT s.id) AS style_id
            FROM films f
                LEFT JOIN films_director fd ON f.id = fd.films_director_films_id
                LEFT JOIN director d ON fd.films_director_director_id = d.id
                LEFT JOIN films_style fs ON f.id = fs.films_style_films_id
                LEFT JOIN style s ON fs.films_style_style_id = s.id
            GROUP BY
                f.id;
        """
        self.dbCursor.execute(sqlStr)
        movies = self.dbCursor.fetchall()
        styleEntity = Style()
        directorEntity = Director()
        listData = []

        for movie in movies:
            directorsList = []
            styleList = []
            if movie[8] != None:
                directorIds = movie[8].split(",")
                for directorId in directorIds:
                    directorsList.append(directorEntity.getBy("id", directorId)[0])

            if movie[9] != None:
                styleIds = movie[9].split(",")
                for styleId in styleIds:
                    styleList.append(styleEntity.getBy("id", styleId)[0])

            item = {
                "id": movie[0],
                "films_title": movie[1],
                "films_plot": movie[2],
                "films_release_year": movie[3],
                "films_release_date": movie[4],
                "films_rating": movie[5],
                "films_image_url": movie[6],
                "films_running_time": movie[7],
                "director": directorsList,
                "style": styleList
            }

            listData.append(item)
        json_data = json.loads(json.dumps(listData))
        return json_data, 200

    def getBy(self, attName, attValue):
        sqlStr = f"""
            SELECT
                f.id AS film_id,
                f.films_title AS film_title,
                f.films_plot AS film_plot,
                f.films_release_year AS film_release_year,
                f.films_release_date AS film_release_date,
                f.films_rating AS film_rating,
                f.films_image_url AS film_image_url,
                f.films_running_time AS film_running_time,
                GROUP_CONCAT(DISTINCT d.id) AS director_id,
                GROUP_CONCAT(DISTINCT s.id) AS style_id
            FROM films f
                LEFT JOIN films_director fd ON f.id = fd.films_director_films_id
                LEFT JOIN director d ON fd.films_director_director_id = d.id
                LEFT JOIN films_style fs ON f.id = fs.films_style_films_id
                LEFT JOIN style s ON fs.films_style_style_id = s.id
            WHERE f.{attName} = '{attValue}';
        """
        self.dbCursor.execute(sqlStr)
        movies = self.dbCursor.fetchall()
        styleEntity = Style()
        directorEntity = Director()
        listData = []

        for movie in movies:
            directorsList = []
            styleList = []
            if movie[8] != None:
                directorIds = movie[8].split(",")
                for directorId in directorIds:
                    directorsList.append(directorEntity.getBy("id", directorId)[0])

            if movie[9] != None:
                styleIds = movie[9].split(",")
                for styleId in styleIds:
                    styleList.append(styleEntity.getBy("id", styleId)[0])

            item = {
                "id": movie[0],
                "films_title": movie[1],
                "films_plot": movie[2],
                "films_release_year": movie[3],
                "films_release_date": movie[4],
                "films_rating": movie[5],
                "films_image_url": movie[6],
                "films_running_time": movie[7],
                "director": directorsList,
                "style": styleList
            }

            listData.append(item)
        json_data = json.loads(json.dumps(listData))
        return json_data, 200

    def add(self, inputItem):
        #créer l'objet input item
        filmData = self.strToObj(inputItem)
        filmId = filmData['id']
        #récupérer la liste des styles
        filmStyle = filmData.pop('style')
        #récupérer la liste des directeurs
        filmDirector = filmData.pop('director')
        #retirer l'id
        filmData.pop('id')
        #est ce que l'item existe
        if self.itemExist(filmId, self.dbTableName) is not None:
            #oui : erreur
            return f"Err : ItemId : {filmId} exist in database", 201
            #non :
                #créer l'item
        self.dbCursor.execute(self.createItemSqlStr(filmData, self.dbTableName))
        self.db.commit()
        #est ce qu'il a des directeurs ou des styles associé
        if filmStyle != None:
            for style in filmStyle:
                style = self.strToObj(style)
                styleId = style.pop('id')
                #est ce que ce style ou directeur existe ?
                if self.itemExist(styleId, 'style') is None:
                    #non : Créer le style ou le directeur
                    self.dbCursor.execute(self.createItemSqlStr(style, 'style'))
                    self.db.commit()
                #ajouter le lien entre le film et le style ou le directeur
                self.dbCursor.execute(f"INSERT INTO films_style ('films_style_films_id', 'films_style_style_id') VALUES ({filmId}, {styleId})")
                self.db.commit()
        if filmDirector != None:
            for director in filmDirector:
                director = self.strToObj(director)
                directorId = director.pop('id')
                if self.itemExist(directorId, 'director') is None:
                    self.dbCursor.execute(self.createItemSqlStr(director, 'director'))
                    self.db.commit()
                self.dbCursor.execute(f"INSERT INTO films_director ('films_director_films_id', 'films_director_director_id') VALUES ({filmId}, {directorId})")
                self.db.commit()
        return "ok", 200

    def createItemSqlStr(self, item, dbTableName):
        collumnSqlStr = ""
        valuesSqlStr = ""
        for key, value in item.items():
            collumnSqlStr += f"'{key}',"
            valuesSqlStr += f"'{value}'," if type(value) is str else f"{value}," if value != None else "null,"
        return f"INSERT INTO {dbTableName} ({collumnSqlStr[:-1]}) VALUES ({valuesSqlStr[:-1]})"


    def itemExist(self, id, dbTableName):
        sqlStr = f"SELECT id FROM {dbTableName} WHERE id = {id}"
        resSql = self.dbCursor.execute(sqlStr)
        res = resSql.fetchone()
        return res

    def strToObj(self, data):
        newObj = {}
        for key, value in data:
            newObj[key] = value
        return newObj
class FilmModel(BaseModel):
    id: int | None = None
    films_title: str | None = None
    films_plot: str | None = None
    films_release_year: int | None = None
    films_release_date: str | None = None
    films_rating: int | None = None
    films_image_url: str | None = None
    films_running_time: int | None = None
    director: List[DirectorModel] | None = None
    style: List[StyleModel] | None = None