from flask import Flask
from config import config
from os import path
from os import listdir
from os.path import isfile, join
from flask_sqlalchemy import SQLAlchemy
import pickle

#Obiekt sqlalchemy
db = SQLAlchemy()
#Nazwa bazy danych
DB_NAME = "database.db"

def creat_app(app_config = 'development'):

    app = Flask(__name__)
    app.config.from_object(config[app_config])
    #Połączenie z bazą danych
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # Konfiguracja ta została dodana ponieważ podczas uruchamiania aplikacji pojawiało się ostrzerzenie, że track_modifications będzie nie wsperane w kolejnych akutalizacjach
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    #Tworzenie bazy danych z tabelą Patent
    from .models.patient import Patient
    create_database(app)
    
    #Rejestracja ścierzek url
    from .controller import home
    from .controller import patientController
    from .controller import dashboard

    app.register_blueprint(home.main)
    app.register_blueprint(patientController.patientController)
    app.register_blueprint(dashboard.dash)
    return app

def create_database(app):
    '''
    tworzenie bazy danych w SQLite
    pod warunkiem, że już nie istnieje
    '''
    if not path.exists('app/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

'''
def deploy_model():

    mypath = '../Models_ML/models/'
    path_models = [(f, join(mypath, f)) for f in listdir(mypath) if isfile(join(mypath, f))]

    models = {}
    for name_model, model in path_models:
        with open(model, 'rb') as f_in:
            short_name_model = name_model.replace('.bin','')
            models[short_name_model] = pickle.load(f_in)

    return models
'''
