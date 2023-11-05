import json
import sqlite3
from modules import dbConnector

class style:
    def __init__(self):
        self.db, self.dbCursor = self.dbConnect()
        pass

    def dbConnect(self):
        db = sqlite3.connect("moviesDatabase.db")
        dbCursor = db.cursor()
        return [db, dbCursor]

    def getAll(self):
        sqlStrStyle = "SELECT * FROM style"
        self.dbCursor.execute(sqlStrStyle)
        styles = self.dbCursor.fetchall()
        listData = []
        for row in styles:
            data_dict = {
                "id": row[0],
                "style_name": row[1],
                "style_description": row[2]
            }
            listData.append(data_dict)
        json_data = json.loads(json.dumps(listData))
        return json_data

    def getById(self, id):
        sqlStrStyle = f"SELECT * FROM style WHERE id = {id};"
        self.dbCursor.execute(sqlStrStyle)
        styles = self.dbCursor.fetchall()
        listData = []
        for row in styles:
            data_dict = {
                "id": row[0],
                "style_name": row[1],
                "style_description": row[2]
            }
            listData.append(data_dict)
        json_data = json.loads(json.dumps(listData))
        return json_data
