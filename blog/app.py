from flask import Flask
from .user.views import user
from .report.views import report
from .article.views import article
from .index.views import index
from .auth.view import auth
from .config import DevelopmentConfig, ProductionConfig
from flask_sqlalchemy import SQLAlchemy
from .extension import db, login_manager
from blog.models import User


VIEWS = [
    index,
    user,
    article,
    report,
    auth
]


def create_app() -> Flask:
    app = Flask(__name__)
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['SECRET_KEY'] = 'xz90d1_%o(g+5x+bhom0w=$=af++&@a6@s21lpla+7*d(3ku96'
    if app.debug == True:
        app.config.from_object(DevelopmentConfig)
        print('run DevelopmentConfig')
    else:
        app.config.from_object(ProductionConfig)
        print('run ProductionConfig')
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    db.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


def register_blueprints(app: Flask):
    for view in VIEWS:
        app.register_blueprint(view)
