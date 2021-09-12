from flask import Flask
from config import config

def creat_app(app_config = 'development'):

    app = Flask(__name__)
    app.config.from_object(config[app_config])
    
    from .controller import home
    from .controller import form

    app.register_blueprint(home.main)
    app.register_blueprint(form.form)
    return app
