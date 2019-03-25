import flask
from flask import Blueprint, g
from peewee import IntegrityError, Model
from werkzeug.utils import secure_filename

# importing related to User & it's forms
from models.user import User
from models.recipe import Recipe
# from models.relationship import Relationship
from instagram_web.blueprints.recipes.forms import RecipeForm, UpdateRecipeForm
from instagram_web.util.s3_helper import upload_file_to_s3, random_file_name

# Common import that shares with the posts.py
from flask import render_template, redirect, url_for, flash, request, session, escape
from flask_login import login_user, logout_user, login_required, current_user
from app import app

# import aws_s3 helper
# from instagram_web.util.s3_helper import upload_file_to_s3, random_file_name

recipes_blueprint = Blueprint('recipes', __name__, template_folder='templates/recipes')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@recipes_blueprint.route('/create', methods=["POST"])
@login_required
def create_recipe():
	recipe_form = RecipeForm()
	if "picture" not in request.files:
		flash("No picture key in request.files", 'danger')
		return redirect(url_for('users.update_user'))
	file = request.files['picture']
	if file.filename == '':
		flash("Please select a file", 'danger')
		return redirect(url_for('users.update_user'))
	if file and allowed_file(file.filename):
		file.filename = secure_filename(file.filename)
		output = upload_file_to_s3(file, app.config['S3_BUCKET'])
		if recipe_form.validate_on_submit():
			new_recipe = Recipe(
				user_id = current_user.id,
				picture=output,
				title = recipe_form.data['title'],
				description = recipe_form.data['description']
			)
			# breakpoint()
			new_recipe.save()
			flash("New recipe created", "success")
			return redirect(url_for('users.index'))
		flash("something went wrong, please try again", "warning")
		return render_template('index.html', recipe_form=recipe_form)

@recipes_blueprint.route('/<int:recipe_id>', methods=['GET'])
def read_recipe(recipe_id):
	form = UpdateRecipeForm()
	that_recipe = Recipe.get_or_none(Recipe.id == recipe_id)
	recipe_user_id = that_recipe.user_id
	return render_template('read_that_recipe.html', recipe=that_recipe, form=form, user=recipe_user_id)

@recipes_blueprint.route('/<int:recipe_id>', methods=['POST'])
@login_required
def edit_recipe(recipe_id):
	form = UpdateRecipeForm()
	that_recipe = Recipe.get_or_none(Recipe.id == recipe_id)
	recipe_owner = User.get_or_none(User.id == that_recipe.user_id)
	if form.validate_on_submit():
		if recipe_owner != current_user:
			flash("Only owner of the recipe can amend the details", "danger")
			return redirect(url_for('read_recipe', recipe_id=recipe_id))
		else:
			if "picture" not in request.files:
				flash("No picture key in request.files", 'danger')
				return redirect(url_for('users.update_user'))
			file = request.files['picture']
			if file.filename == '':
				flash("Please select a file", 'danger')
				return redirect(url_for('users.update_user'))
			if file and allowed_file(file.filename):
				file.filename = secure_filename(file.filename)
				output = upload_file_to_s3(file, app.config['S3_BUCKET'])
			updated_recipe = Recipe.update(
				title=form.data['title'],
				description=form.data['description'],
				picture=output
			).where(Recipe.user_id == recipe_owner.id)
			updated_recipe.execute()
			flash("Recipe updated successfully", "success")
			return redirect(url_for('recipes.read_recipe', recipe_id=recipe_id))
	return render_template('read_that_recipe.html', recipe=that_recipe, form=form)

@recipes_blueprint.route('/delete/<int:recipe_id>', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
	that_recipe = Recipe.get_by_id(recipe_id)
	that_user = User.get_by_id(that_recipe.user_id)
	if that_recipe.user_id != current_user.id:
		flash("Permission denied as you are not the original owner of the recipe", "warning")
		return redirect(url_for('users.that_profile', user=that_user))
	else:
		that_recipe.delete_instance()
		flash(f"Recipe {that_recipe.id} deleted", "success")
		return render_template('display_user.html', user=that_user)
		# return redirect(url_for('users.that_profile', user_id=that_user.id))
	# return redirect(url_for('users.that_profile', user=that_recipe.user_id))
	return render_template('display_user.html', user=that_user)