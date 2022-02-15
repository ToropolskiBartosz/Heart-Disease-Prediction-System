from operator import or_
from os import access
from flask import Blueprint, render_template, request, redirect, url_for
from app.models.patient import Patientbreastcancer,Algoritm,Algoritm_PatientBreastCancer
from sqlalchemy import or_
from app import db
from app.service import predict, controllerservice
from app.form import Formbreastcancer
from app.service.serviceLog import checkFileToPredict

patientBreastCancerController = Blueprint('patientBreastCancerController',__name__)

PATH_BREASTCANCER = './Models_ML/infomodels/breastCancer.csv'
MODEL_PATH_BREASTCANCER = './Models_ML/models/breastCancer'

@patientBreastCancerController.route('/breastCancer/form_predict', methods=['GET','POST'])
def form_predict():
    '''
    Pobieranie informacji z fomularza i następnie
    wykonanie predukcji za pomocą każdego algorytmu.
    Zapisanie również informacje o pacjencie z 
    przewidywaniem zagrozienia w bazie danych SQLite databes.db

    '''
    try:
        form = Formbreastcancer()

        if form.validate_on_submit():
            patient_data = request.form
            models_score = []
            models_score = predict.predict(patient_data,2)

            new_patient = Patientbreastcancer(
                                        cThickness = form.clump_thickness.data,
                                        uofCSize = form.uniformity_of_cell_size.data,
                                        uofShape = form.uniformity_of_cell_shape.data,
                                        mAdhesion = form.marginal_adhesion.data,
                                        sECSize = form.single_epithelial_cell_size.data,
                                        bNuclei = form.bare_nuclei.data,
                                        bChromatin = form.bland_chromatin.data,
                                        nNucleoli = form.normal_nucleoli.data,
                                        mitoses = form.mitoses.data,
                                        access = True,
                                        correct_prediction = None
                                    )

            if not checkFileToPredict('breastcancer',MODEL_PATH_BREASTCANCER,PATH_BREASTCANCER):
                return render_template('info.html',info='Problemy ze spójnością plików')   
            
            #Dodanie do bazy danych
            db.session.add(new_patient)
            
            for param in models_score:
                print(param[0])
                classificator = Algoritm.query.filter_by(model = param[0],type = 'breastcancer',access=True).first()
                new_alg = Algoritm_PatientBreastCancer(patient = new_patient,
                                            algoritmBreastCancer = classificator,
                                            prediction =param[1])
                db.session.add(new_alg)
            db.session.commit()
            
            return render_template('form_predict/predict_result.html', models_score = models_score)
        return render_template('form_predict/form_predict_breastCancer.html',form = form)
    except Exception as e:
        print(f'{e}')
        db.session.rollback()
        return render_template('info.html',info = e)

@patientBreastCancerController.route('/table/breastCancer', methods=['GET','POST'])
def table():
    '''
    Wypisywanie listy pacjentów, wraz z możliwością
    filtrowania danych pod kątem wyników predykcji
    wykonanych przez algorytmy
    '''
    try:
        if request.method == 'GET':
            #Wykonywanie dla GET
            patient_list = Patientbreastcancer.query.filter_by(access=True).all()
            print(patient_list)
            return render_template('patient_list/table_BreastCancer.html', patient_list = patient_list)
        else: 
            #POST
            filtr_table = request.form['filtr']
            patient_list = Patientbreastcancer.query.filter_by(access=True).all()

            correct_patient_list = controllerservice.filtr_table(filtr_table, patient_list)

            return render_template('patient_list/table_BreastCancer.html', patient_list = correct_patient_list)
    except Exception as e:
        print(e)
        return render_template('error.html')

@patientBreastCancerController.route('/table/atrchivesbreastCancer', methods=['GET','POST'])
def atrchives_table():
    try:
        distinctValue = db.session.query(Algoritm.version).filter_by(type='breastcancer',access=False).join(Algoritm_PatientBreastCancer).filter_by(algorytmML_id = Algoritm.id).distinct()
        list_version = [nrVersion[0] for nrVersion in distinctValue] 
        list_version.append('all')
        if request.method == 'GET':
            #Wykonywanie dla GET
            patient_list = Patientbreastcancer.query.filter_by(access=False).all()
            return render_template('patient_list/atrchivestablebreastcancer.html', patient_list = patient_list,listVersion = list_version)
        else: 
            #POST
            filtr_table = request.form['filtr']
            version = request.form['version']
            if version != 'all':
                patient_list = Patientbreastcancer.query.join(Algoritm_PatientBreastCancer).join(Algoritm).filter_by(version=version)
            else:
                patient_list = Patientbreastcancer.query.filter_by(access=False).all()
            correct_patient_list = controllerservice.filtr_table(filtr_table, patient_list)

            return render_template('patient_list/atrchivestablebreastcancer.html',  patient_list = correct_patient_list,listVersion = list_version ) 
    except Exception as e:
        print(f'{e}')
        return render_template('error.html')

@patientBreastCancerController.route('/delete_patient_BreastCancer/<int:patient_id>')
def delete_patient(patient_id):
    '''
    Usuwanie rekordu z bazy danych
    o określonym id
    '''
    try:
        patient = Patientbreastcancer.query.filter_by(id=patient_id).first()
        db.session.delete(patient)
        db.session.commit()

        return render_template('patient_list/delete_patient.html')       
    except:
        return render_template('error.html')


@patientBreastCancerController.route('/update_patient_BreastCancer/<int:patient_id>/<int:predict>')
def update_patient(patient_id,predict):
    try:
        correct_predict = bool(predict)
        
        patient = Patientbreastcancer.query.filter_by(id=patient_id).first()
        patient.correct_prediction = correct_predict
        db.session.commit()
        
        return redirect(url_for('patientBreastCancerController.table'))
    except:
        return render_template('error.html')

    
     