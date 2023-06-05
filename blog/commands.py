import click
from werkzeug.security import generate_password_hash
from blog.extension import db


@click.command('create-init-user')
@click.option('--username', prompt=True, help='The name of the superuser')
@click.option('--email', prompt=True, help='The email address of the superuser')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password for the superuser')
def create_init_user(username, email, password):
    from blog.models import User
    from wsgi import app

    with app.app_context():
        user = User(username=username,
                     first_name=None,
                     last_name=None,
                     email=email,
                     password=generate_password_hash(password),
                     is_admin=False
                     )
        db.session.add(user)
        db.session.commit()

@click.command('create_superuser')
@click.option('--username', prompt=True, help='The name of the superuser')
@click.option('--email', prompt=True, help='The email address of the superuser')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password for the superuser')
def create_superuser(username, email, password):
    from blog.models import User
    from wsgi import app
    with app.app_context():
        admin = User(username=username,
                     first_name=None,
                     last_name=None,
                     email=email,
                     password=generate_password_hash(password),
                     is_admin=True,
                     is_staff=True,
                     )
        db.session.add(admin)
        db.session.commit()


@click.command('delete_user')
@click.option('--user_id', prompt=True, help='id user? type integer')
def delete_user(user_id):
    from blog.models import User
    from wsgi import app
    with app.app_context():
        user = User.query.get(int(user_id))
        db.session.delete(user)
        db.session.commit()

@click.command('create-init-tags')
def create_init_tags():
    from blog.models import Tag
    from wsgi import app

    with app.app_context():
        tags = ('flask', 'django', 'python', 'poetry', 'sqlite')
        for item in tags:
            db.session.add(Tag(name=item))
        db.session.commit()
    click.echo(f'Created tags: {", ".join(tags)}')


