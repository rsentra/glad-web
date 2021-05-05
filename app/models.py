from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class Employee(UserMixin, db.Model):
    """
    Create an Employee table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
  #  first_name = db.Column(db.String(60), index=True)
  #  last_name = db.Column(db.String(60), index=True)
    glad_id = db.Column(db.String(60), index=True, unique=True)
    tel_no = db.Column(db.String(20), index=True)
    password_hash = db.Column(db.String(128))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_admin = db.Column(db.Boolean, default=False)
    posts = db.relationship('Post', backref='author',
                                lazy='dynamic')

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Employee: {}>'.format(self.username)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))


class Department(db.Model):
    """
    Create a Department table
    """

    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='department',
                                lazy='dynamic')

    def __repr__(self):
        return '<Department: {}>'.format(self.name)


class Role(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='role',
                                lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)

class Cars(db.Model):
    """
    Create a Cars table
    """

    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True)

    fc_id = db.Column(db.String(20))
    company = db.Column(db.String(30))
    customer_name = db.Column(db.String(50))
    customer_id = db.Column(db.String(20))
    customer_address = db.Column(db.String(120))
    customer_telno = db.Column(db.String(15))
    customer_job = db.Column(db.String(50))
    customer_eq = db.Column(db.Boolean())
    owner_name = db.Column(db.String(50))
    owner_id = db.Column(db.String(20))
    owner_address = db.Column(db.String(120))
    owner_telno = db.Column(db.String(15))
    owner_job = db.Column(db.String(50))
    car_no = db.Column(db.String(20))
    car_name = db.Column(db.String(50))
    car_code = db.Column(db.String(10))
    car_year = db.Column(db.String(5))
    car_acc = db.Column(db.String(100))
    age_limit = db.Column(db.String(10))
    driver_limit = db.Column(db.String(10))
    driver_name = db.Column(db.String(50))
    driver_id = db.Column(db.String(20))
    cov_mandatory = db.Column(db.Boolean())
    cov_person = db.Column(db.Boolean())
    cov_object = db.Column(db.String(10))
    cov_self = db.Column(db.String(10))
    cov_car = db.Column(db.String(10))
    cov_noncover = db.Column(db.String(10))
    spc_emergency = db.Column(db.String(10))
    spc_blackbox = db.Column(db.Boolean())
    spc_mileage = db.Column(db.Boolean())
    filename = db.Column(db.String(100))
    description = db.Column(db.Text)
    exp_date = db.Column(db.Date)
    created = db.Column(db.DateTime)
    status = db.Column(db.String(10))
    rst_company = db.Column(db.String(30))
    rst_date = db.Column(db.Date)
    updated = db.Column(db.DateTime)
    proc_id = db.Column(db.String(20))
    brh_name = db.Column(db.String(30))
    rt_cause = db.Column(db.String(120))

    def __repr__(self):
        return '<Cars: {}>'.format(self.customer_name)

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer,db.ForeignKey('employees.id'))
    created = db.Column(db.TIMESTAMP)
    title=db.Column(db.String(200))
    body=db.Column(db.Text)
    filename=db.Column(db.String(100))

## MP사번 테이블--회원가입 체크용
class GladFc(db.Model):
    __tablename__ = 'gladfc'
    id = db.Column(db.Integer, primary_key=True)
    glad_id=db.Column(db.String(20))
    glad_name=db.Column(db.String(60))
    glad_brh=db.Column(db.String(100))
    tel_no=db.Column(db.String(20))
