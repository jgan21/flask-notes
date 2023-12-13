from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length


class RegisterUserForm(FlaskForm):
    """Register User Form"""

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(max = 20)]
    )
    # TODO: Length restriction on password????
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min = 8, max = 20)]
    )

    email = StringField(
        "Email",
        validators=[InputRequired(), Email(), Length(max = 50)]
    )

    first_name = StringField(
        "First Name",
        validators=[InputRequired(),Length(max = 30)]
    )

    last_name = StringField(
        "Last Name",
        validators=[InputRequired(), Length(max = 30)]
    )

class LoginUserForm (FlaskForm):
    """Login User Form"""

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(max = 20)]
    )
    # TODO: Length restriction on password????
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min = 8, max = 20)]
    )

class CSRFProtectForm(FlaskForm):
    """Form just for CSRF Protection"""