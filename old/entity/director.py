import json
import sqlite3
from modules import dbConnector

class director:
    def __init__(self):
        self.db, self.dbCursor = self.dbConnect()
        pass

    def dbConnect(self):
        db = sqlite3.connect("moviesDatabase.db")
        dbCursor = db.cursor()
        return [db, dbCursor]

    def getAll(self):
        sqlStrDirector = "SELECT * FROM director"
        self.dbCursor.execute(sqlStrDirector)
        directors = self.dbCursor.fetchall()
        listData = []
        for row in directors:
            data_dict = {
                "id": row[0],
                "director_first_name": row[1],
                "director_last_name": row[2],
                "director_is_awarded": row[3],
                "director_birth_date": row[4]
            }
            listData.append(data_dict)
        json_data = json.loads(json.dumps(listData))
        return json_data

    def getById(self, id):
        sqlStrDirector = f"SELECT * FROM director WHERE id = {id};"
        self.dbCursor.execute(sqlStrDirector)
        directors = self.dbCursor.fetchall()
        listData = []
        for row in directors:
            data_dict = {
                "id": row[0],
                "director_first_name": row[1],
                "director_last_name": row[2],
                "director_is_awarded": row[3],
                "director_birth_date": row[4]
            }
            listData.append(data_dict)
        json_data = json.loads(json.dumps(listData))
        return json_data
