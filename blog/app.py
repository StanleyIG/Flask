from flask import Flask
from blog.user.views import user
from blog.report.views import report
from blog.article.views import article
from blog.index.views import index


def create_app() -> Flask:
    app = Flask(__name__)
    register_blueprints(app)
    return app


def register_blueprints(app: Flask):
    app.register_blueprint(user)
    app.register_blueprint(report)
    app.register_blueprint(article)
    app.register_blueprint(index)
