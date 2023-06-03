from flask_combo_jsonapi import ResourceList, ResourceDetail

from blog.extension import db
from blog.models import Article
from blog.schemas.article import ArticleSchema


class ArticleList(ResourceList):
    schema = ArticleSchema
    data_layer = {
        'session': db.session,
        'model': Article,
    }


class ArticleDetail(ResourceDetail):
    schema = ArticleSchema
    data_layer = {
        'session': db.session,
        'model': Article,
    }