import json
import sqlite3
from modules import dbConnector

class films:
    def __init__(self):
        self.db, self.dbCursor = self.dbConnect()
        pass

    def dbConnect(self):
        db = sqlite3.connect("moviesDatabase.db")
        dbCursor = db.cursor()
        return [db, dbCursor]

    def getAll(self):
        sqlStrFilm = """
            SELECT
                f.id AS film_id,
                f.films_title AS film_title,
                f.films_plot AS film_plot,
                f.films_release_year AS film_release_year,
                f.films_release_date AS film_release_date,
                f.films_rating AS film_rating,
                f.films_image_url AS film_image_url,
                f.films_running_time AS film_running_time,
                GROUP_CONCAT(DISTINCT d.director_first_name) AS director_first_name,
                GROUP_CONCAT(DISTINCT d.director_last_name) AS director_last_names,
                GROUP_CONCAT(DISTINCT d.director_is_awarded) AS director_is_awarded,
                GROUP_CONCAT(DISTINCT d.director_birth_date) AS director_birth_date,
                GROUP_CONCAT(DISTINCT s.style_name) AS style_name
            FROM films f
                LEFT JOIN films_director fd ON f.id = fd.films_director_films_id
                LEFT JOIN director d ON fd.films_director_director_id = d.id
                LEFT JOIN films_style fs ON f.id = fs.films_style_films_id
                LEFT JOIN style s ON fs.films_style_style_id = s.id
            GROUP BY
                f.id;
                """
        self.dbCursor.execute(sqlStrFilm)
        movies = self.dbCursor.fetchall()
        listData = []
        for row in movies:
            direcors = {
                "director_first_name": row[8],
                "director_last_name": row[9],
                "director_is_awarded": row[10],
                "director_birth_date": row[11]
            }

            styles = []
            styleList = row[12].split(",")
            for style in styleList:
                sqlStrStyle = "SELECT * from style WHERE style_name = '" + style + "'"
                self.dbCursor.execute(sqlStrStyle)
                resStyle = self.dbCursor.fetchone()
                styleItem = {
                    "style_name": resStyle[1],
                    "style_description": resStyle[2]
                }
                styles.append(styleItem)

            data_dict = {
                "id": row[0],
                "films_title": row[1],
                "films_plot": row[2],
                "films_release_year": row[3],
                "films_release_date": row[4],
                "films_rating": row[5],
                "films_image_url": row[6],
                "films_running_time": row[7],
                "directors": direcors,
                "styles": styles
            }
            listData.append(data_dict)
        json_data = json.loads(json.dumps(listData))
        return json_data

    def getById(self, id):
        sqlStrFilm = f"""
            SELECT
                f.id AS film_id,
                f.films_title AS film_title,
                f.films_plot AS film_plot,
                f.films_release_year AS film_release_year,
                f.films_release_date AS film_release_date,
                f.films_rating AS film_rating,
                f.films_image_url AS film_image_url,
                f.films_running_time AS film_running_time,
                GROUP_CONCAT(DISTINCT d.director_first_name) AS director_first_name,
                GROUP_CONCAT(DISTINCT d.director_last_name) AS director_last_names,
                GROUP_CONCAT(DISTINCT d.director_is_awarded) AS director_is_awarded,
                GROUP_CONCAT(DISTINCT d.director_birth_date) AS director_birth_date,
                GROUP_CONCAT(DISTINCT s.style_name) AS style_name
            FROM films f
                LEFT JOIN films_director fd ON f.id = fd.films_director_films_id
                LEFT JOIN director d ON fd.films_director_director_id = d.id
                LEFT JOIN films_style fs ON f.id = fs.films_style_films_id
                LEFT JOIN style s ON fs.films_style_style_id = s.id
            WHERE f.id = {id};
                        """
        self.dbCursor.execute(sqlStrFilm)
        movies = self.dbCursor.fetchall()
        listData = []
        for row in movies:
            direcors = {
                "director_first_name": row[8],
                "director_last_name": row[9],
                "director_is_awarded": row[10],
                "director_birth_date": row[11]
            }

            styles = []
            styleList = row[12].split(",")
            for style in styleList:
                sqlStrStyle = "SELECT * from style WHERE style_name = '" + style + "'"
                self.dbCursor.execute(sqlStrStyle)
                resStyle = self.dbCursor.fetchone()
                styleItem = {
                    "style_name": resStyle[1],
                    "style_description": resStyle[2]
                }
                styles.append(styleItem)

            data_dict = {
                "id": row[0],
                "films_title": row[1],
                "films_plot": row[2],
                "films_release_year": row[3],
                "films_release_date": row[4],
                "films_rating": row[5],
                "films_image_url": row[6],
                "films_running_time": row[7],
                "directors": direcors,
                "styles": styles
            }
            listData.append(data_dict)
        json_data = json.loads(json.dumps(listData))
        return json_data

    def postItem(self, inputItem):
        print(inputItem.id)
        item = {
            "id": inputItem.id,
            "films_title": inputItem.films_title,
            "films_plot": inputItem.films_plot,
            "films_release_year": inputItem.films_release_year,
            "films_release_date": inputItem.films_release_date,
            "films_rating": inputItem.films_rating,
            "films_image_url": inputItem.films_image_url,
            "films_running_time": inputItem.films_running_time,
            "director": inputItem.director,
            "style": inputItem.style
        }
        sqlStrFilm = f"SELECT * FROM films WHERE id = {item['id']}"
        self.dbCursor.execute(sqlStrFilm)
        res = self.dbCursor.fetchone()
        if res != None:
            film = {
                "id": res[0],
                "films_title": res[1],
                "films_plot": res[2],
                "films_release_year": res[3],
                "films_release_date": res[4],
                "films_rating": res[5],
                "films_image_url": res[6],
                "films_running_time": res[7]
            }
            changedValues = {}
            for attrName, attrValue in item.items():
                try:
                    if film[attrName] != item[attrName]:
                        changedValues[attrName] = attrValue
                except:
                    continue
            sqlStrUpdateFilm = "UPDATE films SET "
            i = len(changedValues)
            j = 0
            for attrName, attrValue in changedValues.items():
                if j == i - 1:
                    sqlStrUpdateFilm += attrName + " = '" + str(attrValue) + "'"
                else:
                    sqlStrUpdateFilm += attrName + " = '" + str(attrValue) + "',"
                j += 1
            sqlStrUpdateFilm += f" WHERE id = {item['id']};"
            try:
                self.dbCursor.execute(sqlStrUpdateFilm)
            except:
                print("error sql")
        else:
            sqlStrFilmInput = f""""
                INSERT INTO films VALUES (
                    {item['id']},
                    {item['films_title']}, 
                    {item['films_plot']}),
                    {item['films_release_year']}),
                    {item['films_release_date']}),
                    {item['films_rating']}),
                    {item['films_image_url']}),
                    {item['films_running_time']}
                )
            """
            self.dbCursor.execute(sqlStrFilmInput)
        return {"response:": "OK"}