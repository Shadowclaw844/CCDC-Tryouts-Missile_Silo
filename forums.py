from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import InputRequired, Email, Length, AnyOf


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Email() ])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=5, max=10), AnyOf(['secret', 'password'])])

class SearchForm(FlaskForm):
    query = StringField('Enter the ID here', validators=[InputRequired()])

class AddRocket(FlaskForm):
    destination = SelectField('Where to send the rocket?', choices=[('win10','Windows 10'),('win2016','Windows Server 2016'),('centos','Centos 8'),('debian','Debian 10'),], validators=[InputRequired()])
    comments = StringField('Extra information', validators=[InputRequired(), Length(max=200)])