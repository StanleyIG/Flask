import click
from werkzeug.security import generate_password_hash
from blog.extension import db


@click.command('create-init-user')
def create_init_user():
    from blog.models import User
    from wsgi import app

    with app.app_context():
        db.session.add(
            User(email='name@example2.com', password=generate_password_hash('test1234'))
        )
        db.session.commit()
