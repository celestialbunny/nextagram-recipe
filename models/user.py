from models.base_model import BaseModel
from peewee import ForeignKeyField, Model, CharField, IntegrityError, BooleanField
import datetime
from flask_login import UserMixin

class User(UserMixin, BaseModel):
	username = CharField(unique=True, null=False)
	email = CharField(unique=True, null=False)
	password = CharField(unique=False, null=False)

	def __repr__(self):
		return f"Post('{self.username}, '{self.email}')"