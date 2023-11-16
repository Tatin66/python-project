from entity.Entity import Entity
from pydantic import BaseModel


class Style(Entity):
    def __init__(self):
        model = StyleModel()
        super().__init__("style", model)

    def delete(self, id):
        #récupérer la liste des ellement dans films_style
        sqlStr = f"SELECT id FROM films_style WHERE films_style_films_id = {id}"
        self.dbCursor.execute(sqlStr)
        stylesIds = self.dbCursor.fetchall()
        self.db.commit()
        #supprimer de films_director
        for styleId in stylesIds:
            sqlStr = f"DELETE FROM films_style where id = {styleId[0]}"
            self.dbCursor.execute(sqlStr)
            self.db.commit()
        #supprimer le film
        sqlStr = f"DELETE FROM style where id = {id}"
        self.dbCursor.execute(sqlStr)
        self.db.commit()
        return "Ok", 200
class StyleModel(BaseModel):
    id: int | None = None
    style_name: str | None = None
    style_description: str | None = None
