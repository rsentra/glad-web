# third-party imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#login manager 
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

# local imports
from config import app_config

# db variable , login manager initialization
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)

#config.py - default setting
    if config_name==None:
       config_name = 'production'  
    app.config.from_object(app_config[config_name])   
#instance/config.py - default setting override
    app.config.from_pyfile('config.py')                      

    print('instance!!!! ', app.config['SQLALCHEMY_DATABASE_URI'])
    print('app init starting!!!! ',app_config[config_name])

    Bootstrap(app)
    db.init_app(app)

    # temporary route
    # @app.route('/')
    # def hello_world():
    #     return 'Hello, World!'
    #root대신 로긴 매니저
    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"
    migrate = Migrate(app, db)

    from app import models

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from .cars import cars as cars_blueprint
    app.register_blueprint(cars_blueprint)

    from .blog import blog as blog_blueprint
    app.register_blueprint(blog_blueprint)

    from .sales import sales as sales_blueprint
    app.register_blueprint(sales_blueprint)

    app.debug=True
    return app