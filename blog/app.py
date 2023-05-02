from flask import Flask
from .user.views import user
from .report.views import report
from .article.views import article
from .index.views import index
from .auth.view import auth
from .config import DevelopmentConfig, ProductionConfig
from blog.extension import db, login_manager, migrate, csrf
from blog.models import User
from blog import commands


VIEWS = [
    index,
    user,
    article,
    report,
    auth
]


def create_app() -> Flask:
    app = Flask(__name__)
    if app.debug == True:
        app.config.from_object(DevelopmentConfig)
        print('run DevelopmentConfig')
    else:
        app.config.from_object(ProductionConfig)
        print('run ProductionConfig')
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db, compare_type=True)
    csrf.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


def register_blueprints(app: Flask):
    for view in VIEWS:
        app.register_blueprint(view)


def register_commands(app: Flask):
    app.cli.add_command(commands.create_init_user)
    app.cli.add_command(commands.create_superuser)
    app.cli.add_command(commands.delete_user)
