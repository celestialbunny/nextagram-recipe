from models.base_model import BaseModel
from peewee import CharField
from models.user import User

class Todo(BaseModel):
    todo = CharField(unique=False, null=False)

    def __repr__(self):
        return f"Todo('{self.todo}')"