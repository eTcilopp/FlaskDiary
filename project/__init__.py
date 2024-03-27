from flask import Flask
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from dotenv import dotenv_values
from flask_login import LoginManager

db = SQLAlchemy()


def create_app():
    from .rest_api import rest_api as rest_api_blueprint
    from .auth import auth as auth_blueprint
    from .main import main as main_blueprint
    from .models import User
    config = dotenv_values("./.env")
    app = Flask(__name__)

    app.config['SECRET_KEY'] = config["SECRET_KEY"]
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:P@ssw0rd!@57e25356155c:3306/mariadb_flask'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    
    csrf = CSRFProtect(app)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(auth_blueprint)

    app.register_blueprint(main_blueprint)

    app.register_blueprint(rest_api_blueprint)
    csrf.exempt(rest_api_blueprint)

    return app


