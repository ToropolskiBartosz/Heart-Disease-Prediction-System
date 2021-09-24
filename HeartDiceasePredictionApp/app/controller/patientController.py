from operator import or_
from flask import Blueprint, render_template, request
from flask_sqlalchemy import model
from app.models.patient import Patient
from sqlalchemy import or_
from app import db
from app.service import predict

patientController = Blueprint('patientController',__name__)


@patientController.route('/form_predict', methods=['GET','POST'])
def form_predict():
    '''
    Pobieranie informacji z fomularza i następnie
    wykonanie predukcji za pomocą każdego algorytmu.
    Zapisanie również informacje o pacjencie z 
    przewidywaniem zagrozienia w bazie danych SQLite databes.db
    '''
    try:
        if request.method == 'POST':
            #Wykonywanie dla POST
            patient_data = request.form

            models_score = []
            models_score = predict.predict_dicease(patient_data)

            new_patient = Patient(
                                        age = request.form['age'],
                                        sex = request.form['sex'],
                                        cp = request.form['cp'],
                                        trestbps = request.form['trestbps'],
                                        chol = request.form['chol'],
                                        fbs = request.form['fbs'],
                                        restecg = request.form['restecg'],
                                        thalach = request.form['thalach'],
                                        exang = request.form['exang'],
                                        oldpeak = request.form['oldpeak'],
                                        slope = request.form['slope'],
                                        ca = request.form['ca'],
                                        thal = request.form['thal'],
                                        decisiontree =models_score[0][1],
                                        knn =models_score[1][1],
                                        logisticregression =models_score[2][1],
                                        mlp =models_score[3][1],
                                        randomforest =models_score[4][1],
                                        scv = models_score[5][1]
                                    )
            #Dodanie do bazy danych
            db.session.add(new_patient)
            db.session.commit()
                
            return render_template('form_predict/predict_result.html', models_score = models_score)
        else:
            #Wykonywanie GET
            return render_template('form_predict/form_predict.html')

    except:
        return render_template('error.html')



@patientController.route('/table', methods=['GET','POST'])
def table():
    '''
    Wypisywanie listy pacjentów, wraz z możliwością
    filtrowania danych pod kątem wyników predykcji
    wykonanych przez algorytmy
    '''
    try:
        if request.method == 'GET':
            #Wykonywanie dla GET
            patient_list = Patient.query.all()
            return render_template('patient_list/table.html', patient_list = patient_list)

        else: 
            #POST
            filtr_table = request.form['filtr']

            if filtr_table == 'all':
                #Wypisanie wszystkich rekordów
                patient_list = Patient.query.all()
                return render_template('patient_list/table.html', patient_list = patient_list)

            elif filtr_table == 'allr':
                #Wypisanie rekordów bez prawdopodobieństwa zagrożenia
                patient_list = Patient.query.filter_by(decisiontree = False,
                                                        knn = False,
                                                        logisticregression = False,
                                                        mlp = False,
                                                        randomforest =False,
                                                        scv = False)

                return render_template('patient_list/table.html', patient_list = patient_list)

            elif filtr_table == 'dan':
                #Wypisanie rekordów gdzie istnieje jakieś zagrożenie
                #Przynajmnie jedna pozytywna predykcja przewidziana przez algorytm 
                patient_list = Patient.query.filter_by(decisiontree = True,
                                                        knn = True,
                                                        logisticregression = True,
                                                        mlp = True,
                                                        randomforest =True,
                                                        scv = True)
                return render_template('patient_list/table.html', patient_list = patient_list) 

            else:
                #Wypisywanie wszystkich rekordów z niebezpeczeństem
                #Wszystkie predykcjie były pozytywne
                patient_list = Patient.query.filter(or_(Patient.decisiontree == True,
                                                        Patient.knn == True,
                                                        Patient.logisticregression == True,
                                                        Patient.mlp == True,
                                                        Patient.randomforest == True,
                                                        Patient.scv == True)).filter(or_(Patient.decisiontree == False,
                                                                                        Patient.knn == False,
                                                                                        Patient.logisticregression == False,
                                                                                        Patient.mlp == False,
                                                                                        Patient.randomforest == False,
                                                                                        Patient.scv == False))


                return render_template('patient_list/table.html', patient_list = patient_list)

    except:
        return render_template('error.html')


@patientController.route('/delete_patient/<int:patient_id>')
def delete_patient(patient_id):
    '''
    Usuwanie rekordu z bazy danych
    o określonym id
    '''
    try:
        patient = Patient.query.filter_by(id=patient_id).first()
        db.session.delete(patient)
        db.session.commit()

        return render_template('patient_list/delete_patient.html')
        
    except:
        return render_template('error.html')        