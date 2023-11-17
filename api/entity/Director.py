from entity.Entity import Entity
from pydantic import BaseModel


class Director(Entity):
    def __init__(self):
        model = DirectorModel()
        super().__init__("director", model)

    def delete(self, id):
        #récupérer la liste des ellement dans films_director
        sqlStr = f"SELECT id FROM films_director WHERE films_director_films_id = {id}"
        self.dbCursor.execute(sqlStr)
        directorsIds = self.dbCursor.fetchall()
        self.db.commit()
        #supprimer de films_director
        for directorId in directorsIds:
            sqlStr = f"DELETE FROM films_director where id = {directorId[0]}"
            self.dbCursor.execute(sqlStr)
            self.db.commit()
        #supprimer le film
        sqlStr = f"DELETE FROM director where id = {id}"
        self.dbCursor.execute(sqlStr)
        self.db.commit()
        return "Ok"


class DirectorModel(BaseModel):
    id: int | None = None
    director_first_name: str | None = None
    director_last_name: str | None = None
    director_is_awarded: bool | None = None
    director_birth_date: str | None = None
