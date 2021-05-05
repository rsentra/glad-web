import os

from app import create_app   #app/init.py에서 create_app import

config_name = os.getenv('FLASK_CONFIG')
print('This Config Name=',config_name)

app = create_app(config_name)

if __name__ == '__main__':
    print('direct starting------')
    app.run()