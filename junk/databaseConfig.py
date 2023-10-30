import array
import json
import os
import sqlite3
from modules import dbConnector


def dbConnect(self):
    db = sqlite3.connect("../moviesDatabase.db")
    dbCursor = db.cursor()
    return [db, dbCursor]

def fetchData() -> array:
    dataSet = []
    jsonFile = open('movies.json', 'r', encoding="utf8")
    i = 0
    for line in jsonFile:
        movieData = json.loads(line.replace("\n", ""))
        movie = {
            "id": i,
            "title": movieData["title"],
            "plot": movieData["plot"],
            "year": movieData["year"],
            "date": movieData["release_date"],
            "rating": movieData["rating"],
            "directors": str(movieData["directors"]).replace("[", "").replace("]", "").replace("'", "").split(","),
            "style": str(movieData["genres"]).replace("[", "").replace("]", "").replace("'", "").split(","),
            "image": "null" if movieData["image"] == None else movieData["image"],
            "time": movieData["running_time_secs"]
        }

        dataSet.append(movie)
        i += 1
    jsonFile.close()
    return dataSet

def dbCreation():
    dirContent = os.listdir('tablesCreationScript')
    db, dbCursor = dbConnect()
    #db = sqlite3.connect("../moviesDatabase.db")
    #dbCursor = db.cursor()
    for file in dirContent:
        scriptFile = open('tablesCreationScript/'+file)
        scriptContent = scriptFile.read()
        try:
            dbCursor.execute("DROP TABLE " + file[:-4])
        except:
            print("no table :" + file[:-4] + " to delete")
        try:
            dbCursor.execute(scriptContent)
        except Exception as e:
            print(f"Unexpected {e=}, {type(e)=}")
        scriptFile.close()
    dbCursor.close()

def dataInjection(dataSet):
    for movie in dataSet: #pour chaque film
        db, dbCursor = dbConnect()
        #ajouter la table film
        movie["title"] = "null" if movie["title"] == None else movie["title"].replace("'", "''")
        movie["plot"] = "null" if movie["plot"] == None else movie["plot"].replace("'", "''")
        movie["date"] = "null" if movie["date"] == None else movie["date"]
        movie["year"] = "null" if movie["year"] == None else movie["year"]
        movie["time"] = "null" if movie["time"] == None else movie["time"]
        movie["rating"] = "null" if movie["rating"] == None else movie["rating"]

        sqlStr = "INSERT INTO films VALUES ("
        sqlStr += str(movie["id"]) + ", '" + movie["title"] + "', '" + movie["plot"] + "'," + str(movie["year"]) + "," + movie["date"] + "," + str(movie["rating"]) + ", '" + movie["image"] + "'," + str(movie["time"])
        sqlStr += ");"
        try:
            dbCursor.execute(sqlStr)
        except:
            pass
            logFile = open('log.txt', 'a')
            logFile.write("Error in : " + sqlStr + "\n")
            continue
        db.commit()
        db.close()
        #pour chaque directeur
        for directeur in movie["directors"]:
            if directeur == "":
                continue
            if directeur[0] == " ":
                directeur = directeur[1:]
            try:
                firstName, lastName = directeur.split(" ")
            except:
                logFile = open('log.txt', 'a')
                logFile.write("Error in : " + sqlStr + "\n")
            db, dbCursor = dbConnect()
            sqlStr = "SELECT id FROM director WHERE director_first_name == '" + firstName + "';"
            sqlReturn = dbCursor.execute(sqlStr)
            res = dbCursor.fetchone()
            # si le directeur existe pas ajouter le directeur
            if res is None:
                nextIdDirector = dbCursor.execute("SELECT COUNT(*) FROM director;").fetchone()[0]
                sqlStr = "INSERT INTO director VALUES ("
                sqlStr += str(nextIdDirector) + ", '" + firstName + "', '" + lastName + "', null, null"
                sqlStr += ");"
                try:
                    dbCursor.execute(sqlStr)
                except:
                    logFile = open('log.txt', 'a')
                    logFile.write("Error in : " + sqlStr + "\n")
                db.commit()
                db.close()
            else:
                nextIdDirector = res[0]
            #ajouter le lien dans la table film_directeurs
            db, dbCursor = dbConnect()
            nextIdFilmsDirector = dbCursor.execute("SELECT COUNT(*) FROM films_director;").fetchone()[0]
            sqlStr = "INSERT INTO films_director VALUES ("
            sqlStr += str(nextIdFilmsDirector) + ", " + str(movie["id"]) + ", " + str(nextIdDirector)
            sqlStr += ");"
            try:
                dbCursor.execute(sqlStr)
            except:
                logFile = open('log.txt', 'a')
                logFile.write("Error in : " + sqlStr + "\n")
            db.commit()
            db.close()
        #pour chaque style
        for style in movie["style"]:
            style = style.replace(" ", "")
            db, dbCursor = dbConnect()
            sqlStr = "SELECT id FROM style WHERE style_name = '" + style + "';"
            sqlReturn = dbCursor.execute(sqlStr)
            res = dbCursor.fetchone()
            #si le style existe pas ajouter le style
            if res is None:
                nextIdStyle = dbCursor.execute("SELECT COUNT(*) FROM style;").fetchone()[0]
                sqlStr = "INSERT INTO style VALUES ("
                sqlStr += str(nextIdStyle) + ", '" + style + "', null"
                sqlStr += ");"
                try:
                    dbCursor.execute(sqlStr)
                except:
                    logFile = open('log.txt', 'a')
                    logFile.write("Error in : " + sqlStr + "\n")
                db.commit()
                db.close()
            else:
                nextIdStyle = res[0]

            #ajouter le lien dans la table film_style
            db, dbCursor = dbConnect()
            nextIdFilmsStyle = dbCursor.execute("SELECT COUNT(*) FROM films_style;").fetchone()[0]
            sqlStr = "INSERT INTO films_style VALUES ("
            sqlStr += str(nextIdFilmsStyle) + ", " + str(movie["id"]) + ", " + str(nextIdStyle)
            sqlStr += ");"
            try:
                dbCursor.execute(sqlStr)
            except:
                logFile = open('log.txt', 'a')
                logFile.write("Error in : " + sqlStr + "\n")
            db.commit()
            db.close()

dbCreation()
dataInjection(fetchData())
