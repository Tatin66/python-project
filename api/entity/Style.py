from entity.Entity import Entity
from pydantic import BaseModel


class Style(Entity):
    def __init__(self):
        model = StyleModel()
        super().__init__("style", model)
class StyleModel(BaseModel):
    id: int | None = None
    style_name: str | None = None
    style_description: str | None = None
