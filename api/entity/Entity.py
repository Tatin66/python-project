import json
import sqlite3

class Entity():
    def __init__(self, dbTableName, model):
        self.id = None
        self.dbTableName = dbTableName
        self.model = model
        self.db = sqlite3.connect("../moviesDatabase.db")
        self.dbCursor = self.db.cursor()

    def getAll(self):
        sqlStr = f"SELECT * FROM {self.dbTableName};"
        res = self.dbCursor.execute(sqlStr)
        if res != None:
            self.dbCursor.execute(sqlStr)
            resData = self.dbCursor.fetchall()
            listData = []
            for item in resData:
                i = 0
                itemData = {}
                for entityKey, entityValue in self.model:
                    itemData[entityKey] = item[i]
                    i += 1
                listData.append(itemData)
            json_data = json.loads(json.dumps(listData))
            return json_data, 200
        else:
            return "Err: No data to fetch", 100

    def getBy(self, attName, attValue):
        sqlStr = f"SELECT * FROM {self.dbTableName} WHERE {attName} = '{attValue}';"
        res = self.dbCursor.execute(sqlStr)
        if res != None:
            self.dbCursor.execute(sqlStr)
            resData = self.dbCursor.fetchall()
            listData = []
            for item in resData:
                i = 0
                itemData = {}
                for entityKey, entityValue in self.model:
                    itemData[entityKey] = item[i]
                    i += 1
                listData.append(itemData)
            json_data = json.loads(json.dumps(listData[0]))
            pass
            return json_data, 200
        else:
            return "Err: No data to fetch", 100

    def add(self, inputItem):
        sqlStr = f"SELECT id FROM {self.dbTableName} WHERE id = {inputItem.id}"
        resSql = self.dbCursor.execute(sqlStr)
        res = resSql.fetchone()
        print(res)
        if res != None:
            return f"Err: one item already exist with this Id : {inputItem.id}", 200
        collumnSqlStr = ""
        valuesSqlStr = ""
        for key, value in inputItem:
            collumnSqlStr += f"'{key}',"
            valuesSqlStr += f"'{value}'," if type(value) is str else f"{value}," if value != None else "null,"
        sqlStr = f"INSERT INTO {self.dbTableName} ({collumnSqlStr[:-1]}) VALUES ({valuesSqlStr[:-1]})"
        return "Ok", 200