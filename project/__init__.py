from flask import Flask
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from dotenv import dotenv_values
from flask_login import LoginManager
import os
from flask_migrate import Migrate
from flask_moment import Moment

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    from .rest_api import rest_api as rest_api_blueprint
    from .auth import auth as auth_blueprint
    from .main import main as main_blueprint
    from .models import User
    config = dotenv_values("./.env")
    app = Flask(__name__)
    moment = Moment(app)

    app.config['SECRET_KEY'] = config["SECRET_KEY"]
    if os.environ.get('DOCKER_CONTAINER') == '1':
        app.config['SQLALCHEMY_DATABASE_URI'] =\
            f"mysql://{os.environ['MYSQL_USER']}:{os.environ['MYSQL_PASSWORD']}@db/{os.environ['MYSQL_DATABASE']}"
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
        # TODO: For connecting from local to remote DB
        # app.config['SQLALCHEMY_DATABASE_URI'] = \
        #     f"mysql://{os.environ['MYSQL_USER']}:{os.environ['MYSQL_PASSWORD']}@{db_ip_address}/{os.environ['MYSQL_DATABASE']}"
        app.config['SQLALCHEMY_DATABASE_URI'] = \
            f"mysql://{os.environ['MYSQL_USER']}:{os.environ['MYSQL_PASSWORD']}@10.0.0.220/{os.environ['MYSQL_DATABASE']}"
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    csrf = CSRFProtect(app)

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # return User.query.get(int(user_id))
        return User.query.get(user_id)

    app.register_blueprint(auth_blueprint)

    app.register_blueprint(main_blueprint)

    app.register_blueprint(rest_api_blueprint)
    csrf.exempt(rest_api_blueprint)

    return app


