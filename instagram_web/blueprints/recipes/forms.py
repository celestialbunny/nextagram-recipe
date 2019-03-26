from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class RecipeForm(FlaskForm):
	picture = FileField(
		'Picture',
		validators=[
			FileAllowed(['jpg', 'png', 'jpeg'])
		]
	)
	title = StringField(
		'Title',
		validators=[
			DataRequired()
		]
	)
	description = TextAreaField(
		'Description',
		validators=[
			DataRequired()
		]
	)
	btn = SubmitField('Create Recipe')

class UpdateRecipeForm(FlaskForm):
	picture = FileField(
		'Picture',
		validators=[
			FileAllowed(['jpg', 'png', 'jpeg'])
		]
	)
	title = StringField(
		'Title',
		validators=[
			DataRequired()
		]
	)
	description = TextAreaField(
		'Description',
		validators=[
			DataRequired()
		]
	)
	btn = SubmitField('Edit Recipe')