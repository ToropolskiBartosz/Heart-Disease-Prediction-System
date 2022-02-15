from os import access
from platform import version
from flask import Blueprint, render_template, request, redirect, url_for
from app.models.patient import Patient, Algoritm_Patient,Algoritm
from app import db
from app.service import predict, controllerservice
from app.form import FormHeardDicease
from app.service.serviceLog import checkFileToPredict

patientController = Blueprint('patientController',__name__)

PATH_HEARTDICEASE = './Models_ML/infomodels/heartdisease.csv'
MODEL_PATH = './Models_ML/models/heartdisease'

@patientController.route('/heartDisease/form_predict', methods=['GET','POST'])
def form_predict():
    '''
    Pobieranie informacji z fomularza i następnie
    wykonanie predukcji za pomocą każdego algorytmu.
    Zapisanie również informacje o pacjencie z 
    przewidywaniem zagrozienia w bazie danych SQLite databes.db
    '''
    try:
        form = FormHeardDicease()
        if form.validate_on_submit():

            patient_data = request.form

            models_score = []
            models_score = predict.predict(patient_data,1)

            new_patient = Patient(
                                age = form.age.data,
                                sex = form.sex.data,
                                cp = form.cp.data,
                                trestbps = form.trestbps.data,
                                chol = form.chol.data,
                                fbs = form.fbs.data,
                                restecg = form.restecg.data,
                                thalach = form.thalach.data,
                                exang = form.exang.data,
                                oldpeak = form.oldpeak.data,
                                slope = form.slope.data,
                                ca = form.ca.data,
                                thal = form.thal.data,
                                access = True,
                                correct_prediction = None
                                    )

            if not checkFileToPredict('heartdicease',MODEL_PATH,PATH_HEARTDICEASE):
                return render_template('info.html',info='Problemy ze spójnością plików')

            #Dodanie do bazy danych
            db.session.add(new_patient)

            for param in models_score:
                print(param[0])
                classificator = Algoritm.query.filter_by(model = param[0],type='heartdicease',access=True).first()
                new_alg = Algoritm_Patient(patient = new_patient,
                                            algoritmHeard = classificator,
                                            prediction =param[1])
                db.session.add(new_alg)
            db.session.commit()
            
            return render_template('form_predict/predict_result.html', models_score = models_score)
        return render_template('form_predict/form_predict.html',form=form)
    except Exception as e:
        print(e)
        db.session.rollback()
        return render_template('info.html',info = e)



@patientController.route('/table/heartDisease', methods=['GET','POST'])
def table():
    '''
    Wypisywanie listy pacjentów, wraz z możliwością
    filtrowania danych pod kątem wyników predykcji
    wykonanych przez algorytmy
    '''
    try:
        if request.method == 'GET':
            #Wykonywanie dla GET
            patient_list = Patient.query.filter_by(access=True).all()
            
            return render_template('patient_list/table.html', patient_list = patient_list)
        else: 
            #POST
            filtr_table = request.form['filtr']
            patient_list = Patient.query.filter_by(access=True).all()

            correct_patient_list = controllerservice.filtr_table(filtr_table, patient_list)

            return render_template('patient_list/table.html',  patient_list = correct_patient_list) 
    except Exception as e:
        print(f'{e}')
        return render_template('error.html')

@patientController.route('/table/atrchivesheartDisease', methods=['GET','POST'])
def atrchives_table():
    try:
        distinctValue = db.session.query(Algoritm.version).filter_by(type='heartdicease',access=False).join(Algoritm_Patient).filter_by(algorytmML_id = Algoritm.id).distinct()
        list_version = [nrVersion[0] for nrVersion in distinctValue]
        list_version.append('all')
        if request.method == 'GET':
            #Wykonywanie dla GET
            patient_list = Patient.query.filter_by(access=False).all()
            
            return render_template('patient_list/atrchivestable.html', patient_list = patient_list,listVersion = list_version)
        else: 
            #POST
            filtr_table = request.form['filtr']
            version = request.form['version']
            if version != 'all':
                patient_list = Patient.query.join(Algoritm_Patient).join(Algoritm).filter_by(version=version)
            else:
                patient_list = Patient.query.filter_by(access=False).all()

            correct_patient_list = controllerservice.filtr_table(filtr_table, patient_list)

            return render_template('patient_list/atrchivestable.html',  patient_list = correct_patient_list,listVersion = list_version ) 
    except Exception as e:
        print(f'{e}')
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


@patientController.route('/update_patient/<int:patient_id>/<int:predict>')
def update_patient(patient_id,predict):
    try:
        
        correct_predict = bool(predict)

        patient = Patient.query.filter_by(id=patient_id).first()
        if patient == None: print('Patient:')
        patient.correct_prediction = correct_predict
        db.session.commit()
        return redirect(url_for('patientController.table'))
    except:
        return render_template('error.html')    