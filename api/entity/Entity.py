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
        sqlStr = f"SELECT * FROM {self.dbTableName}"
        res = self.dbCursor.execute(sqlStr)
        if res != None:
            resData = self.dbCursor.fetchall()
            self.db.commit()
            listData = []
            for item in resData:
                i = 0
                itemData = {}
                for entityKey, entityValue in self.model:
                    itemData[entityKey] = item[i]
                    i += 1
                listData.append(itemData)
            json_data = json.loads(json.dumps(listData))
            return json_data
        else:
            self.db.commit()
            return "Err: No data to fetch"

    def getBy(self, attName, attValue):
        sqlStr = f"SELECT * FROM {self.dbTableName} WHERE {attName} = '{attValue}';"
        res = self.dbCursor.execute(sqlStr)
        if res != None:
            resData = self.dbCursor.fetchall()
            self.db.commit()
            listData = []
            if (len(resData) == 0):
                return f"Error : Id didn't exist on the table '{self.dbTableName}'"
            for item in resData:
                i = 0
                itemData = {}
                for entityKey, entityValue in self.model:
                    itemData[entityKey] = item[i]
                    i += 1
                listData.append(itemData)
            json_data = json.loads(json.dumps(listData[0]))
            return json_data
        else:
            self.db.commit()
            return "Err: No data to fetch"

    def add(self, inputItem):
        res = None
        if inputItem.id is not None:
            sqlStr = f"SELECT id FROM {self.dbTableName} WHERE id = {inputItem.id}"
            resSql = self.dbCursor.execute(sqlStr)
            res = resSql.fetchone()
        if res != None:
            return f"Err: one item already exist with this Id : {inputItem.id}"
        collumnSqlStr = ""
        valuesSqlStr = ""
        for key, value in inputItem:
            if value != None:
                collumnSqlStr += f"'{key}',"
                valuesSqlStr += f"'{value}'," if type(value) is str else f"{value}," if value != None else "null,"
        sqlStr = f"INSERT INTO {self.dbTableName} ({collumnSqlStr[:-1]}) VALUES ({valuesSqlStr[:-1]})"
        resSql = self.dbCursor.execute(sqlStr)
        return "Ok"

    def modify(self, inputItem):
        if inputItem.id is None:
            return "Error: no Id given"
        #supprimer l'entité
        self.delete(inputItem.id)
        self.db.commit()
        #ajouter l'entité
        self.add(inputItem)
        self.db.commit()
        return "Ok"

    def delete(self, id):
        sqlStr = f"DELETE FROM {self.dbTableName} where id = {id}"
        resSql = self.dbCursor.execute(sqlStr)
        return "Ok"

    def strToObj(self, data):
        newObj = {}
        for key, value in data:
            newObj[key] = value
        return newObj

    def createItemSqlStr(self, item, dbTableName):
        collumnSqlStr = ""
        valuesSqlStr = ""
        for key, value in item.items():
            collumnSqlStr += f"'{key}',"
            valuesSqlStr += f"'{value}'," if type(value) is str else f"{value}," if value != None else "null,"
        return f"INSERT INTO {dbTableName} ({collumnSqlStr[:-1]}) VALUES ({valuesSqlStr[:-1]})"


    def itemExist(self, id, dbTableName):
        if id is not None:
            sqlStr = f"SELECT id FROM {dbTableName} WHERE id = {id}"
            resSql = self.dbCursor.execute(sqlStr)
            res = resSql.fetchone()
        else:
            res = None
        return res