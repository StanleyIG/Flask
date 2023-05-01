from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import logout_user, login_user, login_required, current_user
from werkzeug.security import check_password_hash
from blog.models import User
from blog.forms.user import UserRegisterForm, LoginForm
from flask_wtf.csrf import generate_csrf


auth = Blueprint('auth', __name__, static_folder='../static')


@auth.route('/login', methods=('GET',))
def login():
    errors = []
    if current_user.is_authenticated:
        return redirect(url_for('user.profile', pk=current_user.id))

    form = LoginForm(request.form)
    return render_template(
        'auth/login.html',
        form=form,
        errors=errors
    )


@auth.route('/login', methods=('POST',))
def login_post():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash('Check your login details')
            return redirect(url_for('.login'))

        login_user(user)
        return redirect(url_for('user.profile', pk=user.id))
    else:
        flash('Invalid form data')
        return redirect(url_for('.login'))



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('.login'))