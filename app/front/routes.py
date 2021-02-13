from flask import render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_required
)
from os import environ

from app import login_manager
from app.front import blueprint
from app.back.models.forms import LoginForm
from app.back.models.user import require_admin

# Landing page


@blueprint.route('/')
def route_default():
    return redirect(url_for('front_blueprint.login'))

# Login page


@blueprint.route('/login', methods=['GET'])
def login():
    login_form = LoginForm(request.form)
    if not current_user.is_authenticated:
        return render_template(
            'login/login.html',
            login_form=login_form,
            environ=environ
        )
    return redirect(url_for('front_blueprint.index'))

# Index page


@blueprint.route('/index')
@login_required
def index():
    return render_template('pages/index.html')

# Admin page


@blueprint.route('/users')
@login_required
@require_admin()
def users():
    return render_template('pages/users.html')

# Render all templates

@blueprint.route('/<template>')
@login_required
def route_template(template):
    try:
        return render_template('pages/' + template + '.html')
    except Exception as e:
        return render_template('errors/page_404.html'), 404

# Errors


@blueprint.route('/page_<error>')
def route_errors(error):
    return render_template('errors/page_{}.html'.format(error))


@blueprint.route('/not_authorized')
def not_authorized():
    return render_template('errors/page_403.html'), 403


@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('errors/page_403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('errors/page_403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('errors/page_404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('errors/page_500.html'), 500