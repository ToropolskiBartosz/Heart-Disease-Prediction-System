from flask import Flask
from config import config
from os import path
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = "database.db"

def creat_app(app_config = 'development'):

    app = Flask(__name__)
    app.config.from_object(config[app_config])
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # Konfiguracja ta została dodana ponieważ podczas uruchamiania aplikacji pojawiało się ostrzerzenie, że track_modifications będzie nie wsperane w kolejnych akutalizacjach
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .models.patient import Patient
    create_database(app)
    
    from .controller import home
    from .controller import form
    from .controller import table

    app.register_blueprint(home.main)
    app.register_blueprint(form.form)
    app.register_blueprint(table.table)
    return app

def create_database(app):
    if not path.exists('app/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')