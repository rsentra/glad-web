from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError,TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo

from ..models import Employee


class RegistrationForm(FlaskForm):
    """
    Form for users to create new account
    """
    title = StringField('제목', validators=[DataRequired()])
    body  = TextAreaField('내용',  render_kw={"rows": 10, "cols": 1},validators=[DataRequired()])
    submit = SubmitField('Create')

    # def validate_email(self, field):
    #     if Employee.query.filter_by(email=field.data).first():
    #         raise ValidationError('Email is already in use.')

    # def validate_username(self, field):
    #     if Employee.query.filter_by(username=field.data).first():
    #         raise ValidationError('Username is already in use.')
