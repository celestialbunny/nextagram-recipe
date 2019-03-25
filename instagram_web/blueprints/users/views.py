import flask
from flask import Blueprint, g
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from peewee import IntegrityError, Model

# importing related to User & it's forms
from models.user import User
from models.recipe import Recipe
from instagram_web.blueprints.users.forms import RegistrationForm, LoginForm, UpdateDetailsForm
from instagram_web.blueprints.recipes.forms import RecipeForm, UpdateRecipeForm

# Common import that shares with the posts.py
from flask import render_template, redirect, url_for, flash, request, session, escape
from flask_login import login_user, logout_user, login_required, current_user
from app import app

users_blueprint = Blueprint('users',
							__name__,
							template_folder='templates/users')

"""Start of index"""
@users_blueprint.route('/', methods=["GET"])
def index():
	recipes = Recipe.select()
	recipe_form = RecipeForm()
	if current_user.is_authenticated:
		try:
			recipes = Recipe.select()
		except:
			flash("No recipes for the moment!", "info")
		finally:
			return render_template('index.html', recipes=recipes, form=recipe_form)
	else:
		return render_template('index.html', recipes=recipes, form=recipe_form)

@users_blueprint.route('/signup', methods=["GET"])
def get_signup():
	redirect_if_logged_in()
	form = RegistrationForm()
	return render_template('register.html', form=form)

@users_blueprint.route('/signup', methods=["POST"])
def post_signup():
	form = RegistrationForm()
	if form.validate_on_submit():
		# if unique constraint happens, using or as we just need to know whether one of them is taken
		user = User.get_or_none(User.username == form.data['username'])
		email = User.get_or_none(User.email == form.data['email'])
		if user or email:
			flash("Either username or email has been taken", "danger")
			return redirect(url_for('users.get_signup'))
		else:
			new_user = User(
				username=form.data['username'],
				email=form.data['email'],
				password=generate_password_hash(form.data['password'])
			)
			new_user.save()
			flash("Thanks for registering, you may now log in", "success")
			return redirect(url_for('users.get_login'))
	return render_template('register.html', form=form)

@users_blueprint.route('/login', methods=["GET"])
def get_login():
	form = LoginForm()
	return render_template('login.html', form=form)

@users_blueprint.route('/login', methods=["POST"])
def post_login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.get_or_none(User.email == form.data['email'])
		if user == None:
			flash("There is no account associated with the particular address", "warning")
		else:
			password = check_password_hash(user.password, form.password.data)
			# password = form.password.data
			if password:
				login_user(user)
				flash("You've been logged in!", "success")
				return redirect(url_for('users.index'))
			else:
				flash("Please recheck the password entered", "warning")
				return redirect(url_for('users.get_login'))
	return render_template('login.html', form=form)

@users_blueprint.route('/logout')
@login_required
def logout():
	logout_user()
	flash("Log out successfully!", "success")
	return redirect(url_for('users.index'))

def redirect_if_logged_in():
	if current_user.is_authenticated:
		flash("You have already been logged in", "warning")

@users_blueprint.route('/profile', methods=["GET"])
@login_required
def view_profile():
	# Technically no need to perform any logic as at the "html" side, using {{ current_user }} is sufficient
	form = UpdateDetailsForm()
	return render_template('profile.html', form=form)

# unfortunately flsk-forms does not support PUT/DELETE request... so need to use POST to perform the amendment of profile instead
@users_blueprint.route('/profile', methods=['POST'])
@login_required
def edit_profile():
	# check whether both email and username has been taken, if not update the specific profile
	form = UpdateRecipeForm()

	if check_password_hash(current_user.password, form.data['password']):
		if current_user.username != form.data['username']:
			updated_user = User.update(username=form.data['username']).where(User.id == current_user.id)
			updated_user.execute()
		if current_user.email != form.data['email']:
			updated_user = User.update(email=form.data['email']).where(User.id == current_user.id)
			updated_user.execute()
		if form.data['password'] != form.data['new_password']:
			# updated_user = User.update(password=generate_password_hash(new_password)).where(User == current_user)
			updated_user = User.update(password=generate_password_hash(form.data['new_password'])).where(User.id == current_user.id)
			updated_user.execute()
		flash("Profile successfully updated", "success")
		return redirect(url_for('users.view_profile'))
	else:
		flash("Kindly ensure that the initial password matches", "danger")
		return redirect(url_for('users.view_profile'))
	return redirect(url_for('users.view_profile'))

@users_blueprint.route('/<int:user>', methods=["GET"])
def that_profile(user):
    # that_user = User.get_or_none(User.id == user_id)
    that_user = User.get_or_none(User.id == user)
    recipes = Recipe.select().where(Recipe.user_id == user)
    return render_template('display_user.html', user=that_user, recipes=recipes)