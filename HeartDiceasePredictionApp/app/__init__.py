from flask import Flask
from config import config
from os import path
from os import listdir
from os.path import isfile, join
from flask_sqlalchemy import SQLAlchemy
import pickle
import pandas as pd


#Obiekt sqlalchemy
db = SQLAlchemy()
#Nazwa bazy danych
DB_NAME = "database.db"

def creat_app(app_config = 'development'):

    app = Flask(__name__)
    app.config.from_object(config[app_config])
    #Połączenie z bazą danych
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SECRET_KEY'] = '%MZAST&'
    # Konfiguracja ta została dodana ponieważ podczas uruchamiania aplikacji pojawiało się ostrzerzenie, że track_modifications będzie nie wsperane w kolejnych akutalizacjach
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    #Tworzenie bazy danych 
    from .models.patient import Patient
    from .models.patient import Algoritm
    from .models.patient import Algoritm_Patient
    from .models.patient import Patientbreastcancer
    from .models.patient import Algoritm_PatientBreastCancer
    from .models.patient import Patientthyroid
    from .models.patient import Algoritm_PatientThyroid
 
    if not path.exists('app/' + DB_NAME):
        db.create_all(app=app)
        print('Utworzono baze danych!')

        from .service.addAlgoritm import addAlgoritms
        addAlgoritms(app)

    #Rejestracja ścierzek url
    from .controller import home
    from .controller import patientController
    from .controller import patientBreastCancerController
    from .controller import patientThyroidController
    from .controller import dashboard

    app.register_blueprint(home.main)
    app.register_blueprint(patientController.patientController)
    app.register_blueprint(patientBreastCancerController.patientBreastCancerController)
    app.register_blueprint(patientThyroidController.patientThyroidController)
    app.register_blueprint(dashboard.dash)
    return app


