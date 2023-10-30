import sqlite3

def dbConnect():
    db = sqlite3.connect("../moviesDatabase.db")
    dbCursor = db.cursor()
    return [db, dbCursor]