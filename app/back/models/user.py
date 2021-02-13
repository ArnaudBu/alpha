from bcrypt import gensalt, hashpw
from flask import redirect, url_for
from functools import wraps
from flask_login import UserMixin
from sqlalchemy import Binary, Column, Integer, String, Boolean
from flask_login import current_user

from app import db, login_manager

class User(db.Model, UserMixin):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(Binary)
    admin = Column(Boolean, nullable=False, default=False)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
            if property == 'password':
                value = hashpw(value.encode('utf8'), gensalt())
            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)

    @property
    def serialize(self):
        return {
           'id': self.id,
           'username': self.username,
           'email': self.email,
           'admin': self.admin
           }

    @property
    def is_admin(self):
        return self.admin


@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return user if user else None

# Wrapper for admin access


def require_admin():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_admin:
                return redirect(url_for('front_blueprint.not_authorized'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
