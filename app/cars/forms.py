from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError,BooleanField,SelectField,RadioField,TextField,DateField,validators
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.fields.html5 import DateTimeLocalField

from ..models import Employee

COMPANY_CHOICES = [('삼성', '삼성화재'), ('흥국', '흥국화재'), ('메리츠', '메리츠화재'),('현대', '현대해상'),('DB', 'DB손보'),
                   ('KB', 'KB손보'),('한화', '한화손보'),('롯데', '롯데손보'),('더케이', '더케이손보'),('MG', 'MG손보'),('AXA', 'AXA손보'),('신규', '신규차량') ]
DRIVER_CHOICES=[('누구나', '누구나운전'), ('가족', '가족한정'), ('부부', '부부한정'),('기명1인', '기명피보험자1인한정'),('지정1인', '지정운전자1인한정'),
                ('가족형제', '가족한정+형제자매'), ('기명피보험자+1인', '기명피보험자+기명1인'), ('가족+1인', '가족한정+기명1인'),('부부+1인', '부부한정+기명1인'),('지정1인', '지정운전자1인한정') ]
AGE_CHOICES = [('전연령', '전연령'), ('21세', '만21세 이상'), ('22세', '만22세 이상'),('24세', '만24세 이상'),('26세', '만26세 이상'),
               ('28세', '만28세 이상'), ('30세', '만30세 이상'),('35세', '만35세 이상'),('43세', '만43세 이상'),('48세', '만48세 이상')]
SELF_CHOICES = [('미가입','제외'),('자신1','자기 1천5백/1천5백/1천5백'),('자신2','자기 3천/1천5백/3천'),('자신3','자기 3천/3천/3천'),('자신4','자기 5천/1천5백/5천'),
                ('자신5','자기 5천/3천/5천'),('자신6','자기 5천/5천/5천'),('자신7','자기 1억/1천5백/1억'),('자신8','자기 1억/3천/1억'),('자신9','자기 1억/5천/1억'),
                ('자상1','자상 1억/1천/1억'),('자상2','자상 1억/2천/1억'),('자상3','자상 1억/3천/1억'),('자상4','자상 1억/5천/1억'),('자상5','자상 1억/1억/1억'),
                ('자상6','자상 2억/2천/2억'),('자상7','자상 2억/3천/2억'),('자상8','자상 2억/3천/2억'),('자상9','자상 2억/5천/2억'),('자상10','자상 2억/1억/2억'),
                ('자상11','자상 3억/3천/3억'),('자상12','자상 3억/5천/3억'),('자상13','자상 3억/1억/3억'),('자상14','자상 3억/3억/3억'),('자상15','자상 5억/5억/5억')]
# SELF_CHOICES = [('미가입','제외'),('자신1','자기 1.5/1.5/1.5천')]

class RegistrationForm(FlaskForm):
    """
    Form for users to create new account
    """
      # fc_id = StringField('')
    # company = StringField('보험사',validators=[DataRequired()])
    company = SelectField('보험사',choices=COMPANY_CHOICES) 
    fc_id = StringField('담당FC',validators=[DataRequired()])
    customer_name = StringField('고객이름',validators=[DataRequired()])
    customer_id = StringField('주민번호',validators=[DataRequired(),validators.Length(min=10, max=15)])
    customer_address = StringField('고객주소',validators=[DataRequired()])
    customer_telno = StringField('전화번호',validators=[DataRequired()])
    customer_job = StringField('고객직업')
    customer_eq = BooleanField('계/피동일')
    owner_name = StringField('피보험자',validators=[DataRequired()])
    owner_id = StringField  ('주민번호',validators=[DataRequired()])
    owner_address = StringField('주소',validators=[DataRequired()])
    owner_telno = StringField('전화번호',validators=[DataRequired()])
    owner_job = StringField('직업',validators=[DataRequired()])
    car_no = StringField('차량번호',validators=[DataRequired()])
    car_name = StringField('차명',validators=[DataRequired()])
    car_code = StringField('차명코드')
    car_year = StringField('연식')
    car_acc = StringField('부속품')
    age_limit = SelectField('연령한정',choices= AGE_CHOICES)    
    driver_limit = SelectField('운전범위',choices=DRIVER_CHOICES)    
    driver_name = StringField('지정운전자/배우자')
    driver_id = StringField('주민번호')
    cov_mandatory = BooleanField('의무',default="checked")
    cov_person = BooleanField('대인',default="checked")
    cov_object = SelectField('대물',choices=[('2천','2천'),('3천','3천'),('5천','5천'),('7천','7천'),('1억','1억'),('2억','2억'),('3억','3억'),('5억','5억'),('10억','10억'),('미가입','제외')])
    cov_self = SelectField('상해',choices=SELF_CHOICES)
    cov_car = SelectField('자차',choices=[('20%','20%(20~50만)'),('미가입','제외')])
    cov_noncover = SelectField('무보험',choices=[('2억','2억'),('2억','5억'),('미가입','제외')])
    spc_emergency = SelectField('긴급출동',choices=[('일반','일반형'),('고급','고급형')])
    spc_blackbox = BooleanField('블랙박스')
    spc_mileage = BooleanField('마일리지')
    filename = StringField('첨부파일')
    description = TextField('요청사항')
    exp_date= DateField("보험시작일", format='%Y%m%d',validators=[validators.Optional()])
    submit = SubmitField('Register')

    # def validate_email(self, field):
    #     if Employee.query.filter_by(email=field.data).first():
    #         raise ValidationError('Email is already in use.')

    # def validate_username(self, field):
    #     if Employee.query.filter_by(username=field.data).first():
    #         raise ValidationError('Username is already in use.')
