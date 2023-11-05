from entity.Entity import Entity
from pydantic import BaseModel


class Director(Entity):
    def __init__(self):
        model = DirectorModel()
        super().__init__("director", model)

class DirectorModel(BaseModel):
    id: int | None = None
    director_first_name: str | None = None
    director_last_name: str | None = None
    director_is_awarded: bool | None = None
    director_birth_date: str | None = None
