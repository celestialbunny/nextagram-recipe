import flask
from flask import Blueprint, g
from peewee import IntegrityError, Model
from werkzeug.utils import secure_filename

# importing related to User & it's forms
# from models.user import User
from models.recipe import Recipe
from instagram_web.blueprints.recipes.forms import RecipeForm, UpdateRecipeForm

# Common import that shares with the posts.py
from flask import render_template, redirect, url_for, flash, request, session, escape
from flask_login import login_user, logout_user, login_required, current_user
from app import app

todos_blueprint = Blueprint('todos',
							__name__,
							template_folder='templates/todos')

@todos_blueprint.route('/create/<int:recipe_id>', mthods=['POST'])
def create_todo(recipe_id):
    that_recipe = Recipe.get_or_none(Recipe.id == recipe_id)
    if that_recipe == None:
        flash("Invalid request, please retry", "warning")
        return redirect(url_for('recipes.read_recipe', recipe_id=recipe_id))
