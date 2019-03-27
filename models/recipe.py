from models.base_model import BaseModel
from models.user import User
from peewee import CharField, IntegerField, TextField, ForeignKeyField

class Recipe(BaseModel):
	user = ForeignKeyField(User, backref='recipes')
	picture = CharField(unique=False, null=True)
	title = CharField(unique=False, null=False)
	description = TextField(unique=False, null=False)

	def __repr__(self):
		return f"This recipe titled {self.title}, is {self.description} and tagged under {self.tag}"