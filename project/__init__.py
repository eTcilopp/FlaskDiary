from flask import Flask
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from dotenv import dotenv_values
from flask_login import LoginManager

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


def create_app():
    config = dotenv_values("./.env")
    app = Flask(__name__)

    app.config['SECRET_KEY'] = config["SECRET_KEY"]
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    csrf = CSRFProtect(app)

    db.init_app(app)
    
    from . import models

    with app.app_context():
        db.create_all()
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .rest_api import rest_api as rest_api_blueprint
    app.register_blueprint(rest_api_blueprint)
    csrf.exempt(rest_api_blueprint)
    
    

    return app