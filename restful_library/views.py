from datetime import datetime, timedelta

from flask import render_template, flash, redirect, url_for, request, g
from flask.ext.login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)

from restful_library import app, login_manager, db
from restful_library.forms import LoginForm, ApiTokenForm
from restful_library.models import User, ApiToken


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
@login_required
def main():
    return render_template('api_documentation.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user.is_authenticated():
        return redirect(url_for('main'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not (user and user.check_password(form.password.data)):
            form.email.errors.append('Вы ввели неправильный e-mail/пароль.')
            return render_template('login.html', form=form)

        remember = form.remember.data
        login_user(user, remember=remember)
        flash('Добро пожаловать, {0}'.format(user), category='info')
        return redirect(request.args.get('next') or url_for('main'))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main'))


@app.route('/token_list')
@login_required
def token_list():
    tokens = (
        ApiToken.query
        .order_by(ApiToken.date_created.desc())
        .all()
    )
    return render_template('token_list.html', tokens=tokens)


@app.route('/token/add', methods=['GET', 'POST'])
@login_required
def token_add():
    form = ApiTokenForm()
    if form.validate_on_submit():
        date_expiry = datetime.now() + timedelta(days=form.expiry_days.data)
        token = ApiToken(date_expiry=date_expiry)
        token.description = form.description.data
        token.created_by = g.user
        db.session.add(token)
        db.session.commit()
        flash(u'API Token "{}" создан.'.format(token.uuid), category='success')
        return redirect(url_for('token_list'))
    return render_template('token_add.html', form=form)
