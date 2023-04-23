from blog.app import create_app, db
from werkzeug.security import generate_password_hash


app = create_app()


@app.cli.command("init-db", help="create all db")
def init_db():
    db.create_all()


@app.cli.command("create-users", help="create users")
def create_users():
    from blog.models import User
    db.session.add(
        User(email="name@email.com", password=generate_password_hash("test"))
    )
    db.session.commit()
