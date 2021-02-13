from bcrypt import checkpw
from flask import jsonify, redirect, url_for, request
from flask_login import (
    login_required,
    login_user,
    logout_user
)

from app import db, login_manager
from app.back import blueprint
from app.back.models.user import User, require_admin

# Login & Registration


@blueprint.route('/login', methods=['POST'])
def login():
    if 'login' in request.form:
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and checkpw(password.encode('utf8'), user.password):
            login_user(user)
            return redirect(url_for('front_blueprint.route_default'))
        return redirect(url_for('front_blueprint.route_default'))
    return redirect(url_for('front_blueprint.index'))

# Logout


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('front_blueprint.login'))


# Get users
@blueprint.route('/users', methods=['GET'])
@login_required
@require_admin()
def users():
    users = User.query.all()
    return jsonify(users=[i.serialize for i in users])

# Get one user
@blueprint.route('/user/<id>')
@login_required
@require_admin()
def get_user(id):
    user = User.query.filter_by(id=id).first()
    return jsonify(user=user.serialize)

# Process a user
@blueprint.route('/process_user', methods=['POST'])
@login_required
@require_admin()
def process_user():
    request_form = request.form
    user = User.query.filter_by(id=request_form['id']).first()
    isadmin = False
    if 'admin' in request_form:
        if request_form['admin'] == 'on':
            isadmin = True
    if not user:
        user_data = User(
            email=request_form['email'],
            username=request_form['username'],
            password=request_form['password'],
            admin=isadmin
        )
        db.session.add(user_data)
        db.session.commit()
        return jsonify(user=user_data.serialize)
    else:
        user.email = request_form['email']
        user.username = request_form['username']
        user.admin = isadmin
        db.session.commit()
        return jsonify(user=user.serialize)

# Delete a user
@blueprint.route('/delete_user/<id>')
@login_required
@require_admin()
def delete_user(id):
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()
    return jsonify(user=user.serialize)