from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from ..models import Employee


class RegistrationForm(FlaskForm):
    """
    Form for users to create new account
    """
    customer_name = StringField('고객명', validators=[DataRequired()])
    customer_id = StringField('주민번호', validators=[DataRequired()])
    customer_telno = StringField('전화번호', validators=[DataRequired()])
    customer_address = StringField('주소')

    car_no = StringField('차량번호', validators=[DataRequired()])
    car_name = StringField('차량명')    
    description = StringField('Descriptions here...')    

    submit = SubmitField('Register')

    # def validate_email(self, field):
    #     if Employee.query.filter_by(email=field.data).first():
    #         raise ValidationError('Email is already in use.')

    # def validate_username(self, field):
    #     if Employee.query.filter_by(username=field.data).first():
    #         raise ValidationError('Username is already in use.')
