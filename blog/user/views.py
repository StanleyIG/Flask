from flask import Blueprint, render_template, redirect, url_for, request
from werkzeug.exceptions import NotFound
from flask_login import login_required, current_user, login_user
from blog.models import User
from blog.models import Article
from blog.forms.user import UserRegisterForm
from werkzeug.security import generate_password_hash
from blog.extension import db



user = Blueprint("user", __name__, url_prefix="/users", static_folder="../static")
USERS = {
    1: {"name": "Ivan"},
    2: {"name": "Jon"},
    3: {"name": "Mary"}
}


@user.route('register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user.profile', pk=current_user.id))

    form = UserRegisterForm(request.form)
    errors = []
    if request.method == 'POST' and form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).count():
            form.email.errors.append('email already exists')
            return render_template('users/register.html', form=form)

        _user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            password=generate_password_hash(form.password.data),
            is_admin=False,
        )

        db.session.add(_user)
        db.session.commit()
        login_user(_user)
        return redirect(url_for('auth.login'))

    return render_template(
        'users/register.html',
        form=form,
        errors=errors,
    )


@user.route("/")
@login_required
def user_list():
    users = User.query.all()
    return render_template(
        "users/list.html",
        users=users
    )


@user.route("/<int:pk>")
@login_required
def profile(pk: int):
    _user = User.query.filter_by(id=pk).one_or_none()
    _article = Article.query.filter_by(author_id=_user.id)
    if _user is None:
        raise NotFound("User id:{}, not found".format(pk))
    return render_template(
        "users/details.html",
        user=_user, articles=_article
    )




def get_user_name(pk: int):
    _user = User.query.filter_by(id=pk).one_or_none()
    if _user is None:
        raise NotFound("User id:{}, not found".format(pk))
    return _user
