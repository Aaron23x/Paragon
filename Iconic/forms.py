from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from Iconic.models import User

class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError("Username esists! Please try a different username.")

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError("Email Address already exists! Please try a different email address")
    
    first_name = StringField(label="First Name", validators=[DataRequired()])
    last_name = StringField(label="Last Name", validators=[DataRequired()])
    username = StringField(label="Username", validators=[DataRequired(), Length(min=3, max=15)])
    email_address = StringField(label="Email Address", validators=[DataRequired(), Email()])
    password1 = PasswordField(label="Password", validators=[DataRequired(), Length(min=8, max=20),
                                 EqualTo("password_confirm", message="Password Does Not Match!")])
    password_confirm = PasswordField(label="Confirm Password", validators=[DataRequired()])
    submit = SubmitField(label="Join Paragon")


class LoginForm(FlaskForm):

    username = StringField(label="Username", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Log In")

