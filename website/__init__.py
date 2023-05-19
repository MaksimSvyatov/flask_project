from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy() # make Data base
DB_NAME = 'database.db' # database name

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "helloworld"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # tell flask where is database is
    db.init_app(app) # initialize database

    from .views import views 
    from .auth import auth

    app.register_blueprint(views, url_prefix="/") # Register blueprint
    app.register_blueprint(auth, url_prefix="/") # Register blueprint

    from .models import User, Post, Comment, Like # import all models before creating database

    create_database(app) # call database

    login_manager = LoginManager() # init login manager
    login_manager.login_view = "auth.login" # redirect to login view
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) # need to convert id from string (like in class User) to int

    return app

def create_database(app):
    # if not path.exists("website/" + DB_NAME):
    with app.app_context():
        db.create_all()
        print ("Created database!")