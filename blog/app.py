from flask import Flask
from .user.views import user
from .report.views import report
from .article.views import article
from .index.views import index
from .auth.view import auth
from .author.views import author
from .config import DevelopmentConfig, ProductionConfig
from blog.extension import db, login_manager, migrate, csrf, _admin, api
from blog.models import User, Tag, Article
from blog import commands
from .admin import views
from combojsonapi.spec import ApiSpecPlugin


VIEWS = [
    index,
    user,
    article,
    report,
    auth,
    author,
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
    register_api_routes()
    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db, compare_type=True)
    csrf.init_app(app)
    _admin.init_app(app)
    api.plugins = [
        ApiSpecPlugin(
            app=app,
            tags={
                'Tag': 'Tag API',
                'User': 'User API',
                'Author': 'Author API',
                'Article': 'Article API',
            }
        ),
    ]
    api.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


def register_api_routes():
    from blog.api.tag import TagList
    from blog.api.tag import TagDetail
    from blog.api.user import UserList
    from blog.api.user import UserDetail
    from blog.api.author import AuthorList
    from blog.api.author import AuthorDetail
    from blog.api.article import ArticleList
    from blog.api.article import ArticleDetail

    api.route(TagList, 'tag_list', '/api/tags/', tag='Tag')
    api.route(TagDetail, 'tag_detail', '/api/tags/<int:id>', tag='Tag')

    api.route(UserList, 'user_list', '/api/users/', tag='User')
    api.route(UserDetail, 'user_detail', '/api/users/<int:id>', tag='User')

    api.route(AuthorList, 'author_list', '/api/authors/', tag='Author')
    api.route(AuthorDetail, 'author_detail', '/api/authors/<int:id>', tag='Author')

    api.route(ArticleList, 'article_list', '/api/articles/', tag='Article')
    api.route(ArticleDetail, 'article_detail', '/api/articles/<int:id>', tag='Article')


def register_blueprints(app: Flask):
    for view in VIEWS:
        app.register_blueprint(view)

    _admin.add_view(views.TagAdminView(Tag, db.session))
    _admin.add_view(views.ArticleAdminView(Article, db.session))
    _admin.add_view(views.UserAdminView(User, db.session))

def register_commands(app: Flask):
    app.cli.add_command(commands.create_init_user)
    app.cli.add_command(commands.create_superuser)
    app.cli.add_command(commands.delete_user)
    app.cli.add_command(commands.create_init_tags)