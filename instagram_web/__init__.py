from app import app
from flask import render_template, redirect, url_for
from flask_login import LoginManager
from flask_assets import Environment, Bundle
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.recipes.views import recipes_blueprint
from instagram_web.blueprints.todos.views import todos_blueprint
from .util.assets import bundles
import os
# from instagram_web.util.google_oauth import oauth
import config

from models.user import User

assets = Environment(app)
assets.register(bundles)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'

# oauth.init_app(app)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(recipes_blueprint, url_prefix="/recipes")
app.register_blueprint(todos_blueprint, url_prefix="/todos")

@login_manager.user_loader
def load_user(user_id):
	return User.get_or_none(User.id == user_id)

@app.errorhandler(500)
def error_500(e):
	return render_template('500.html'), 500

@app.errorhandler(405)
def error_405(e):
	return render_template('404.html'), 405

@app.errorhandler(404)
def error_404(e):
	return render_template('404.html'), 404

@app.errorhandler(403)
def error_403(e):
	return render_template('404.html'), 403

@app.route("/")
def home():
	# return render_template('home.html')
	return redirect(url_for('users.index'))
