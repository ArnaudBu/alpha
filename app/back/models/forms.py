from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField

# login and registration

class LoginForm(FlaskForm):
    username = TextField("Username", id='username_login')
    password = PasswordField('Password', id='pwd_login')
