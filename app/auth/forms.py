from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError,SelectField
from wtforms.validators import DataRequired, Email, EqualTo,Length

from ..models import Employee,GladFc

class RegistrationForm(FlaskForm):
    """
    Form for users to create new account
    """
    email = StringField('ID', validators=[DataRequired()])
    username = StringField('이름', validators=[DataRequired()])
    glad_id = StringField('MP 사번', validators=[DataRequired()])
    tel_no = StringField('전화 번호', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
                                        DataRequired(),
                                        EqualTo('confirm_password')
                                        ])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Register')

    def validate_email(self, field):
        if Employee.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use..사용중인 ID입니다')

    def validate_username(self, field):
        if Employee.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use...이미 가입한 이름입니다.')

    def validate_glad_id(self, field):
        if Employee.query.filter_by(glad_id=field.data).first():
            raise ValidationError('glad_id is already in use...이미 가입한 사번입니다.')
        if GladFc.query.filter_by(glad_id=field.data).first() is None:
            raise ValidationError('Your mp ID is invalid...MP사번을 정확히 입력하세요.')
        
class UpdateForm(FlaskForm):
    """
    Form for users to create new account
    """
    email = StringField('ID', render_kw={'readonly': True},validators=[DataRequired()])
    username = StringField('이름', render_kw={'readonly': True},validators=[DataRequired()])
    glad_id = StringField('MP 사번', render_kw={'readonly': True},validators=[DataRequired()])
    role_id = SelectField('Role',choices=[('0','admin'),('1','지점장/실장'),('2','FC')])
    tel_no = StringField('전화 번호', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
                                        DataRequired(),
                                        EqualTo('confirm_password')
                                        ])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Update')

class LoginForm(FlaskForm):
    """
    Form for users to login
    """
    email = StringField('ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')