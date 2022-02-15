from flask import Blueprint, render_template, request, redirect, url_for
from flask_sqlalchemy import model
from app.models.patient import Patientthyroid, Algoritm_PatientThyroid, Algoritm
from app import db
from app.service import predict , controllerservice
from app.form import FormThyroid
from app.service.serviceLog import checkFileToPredict

patientThyroidController = Blueprint('patientThyroidController',__name__)

PATH_THYROID = './Models_ML/infomodels/thyroid.csv'
MODEL_PATH_THYROID = './Models_ML/models/thyroid'

@patientThyroidController.route('/thyroid/form_predict', methods=['GET','POST'])
def form_predict():
    '''
    Pobieranie informacji z fomularza i następnie
    wykonanie predukcji za pomocą każdego algorytmu.
    Zapisanie również informacje o pacjencie z 
    przewidywaniem zagrozienia w bazie danych SQLite databes.db

    '''
    try:
        form = FormThyroid()

        if form.validate_on_submit():
            patient_data = request.form

            models_score = []
            models_score = predict.predict(patient_data,3)

            conversion_boolean = {'0':False,'1':True}

            new_patient = Patientthyroid(
                                        age = form.age.data, 
                                        sex = form.sex.data, 
                                        on_thyroxine = conversion_boolean[form.on_thyroxine.data], 
                                        maybe_on_thyroxine = conversion_boolean[form.maybe_on_thyroxine.data], 
                                        on_antithyroid_medication = conversion_boolean[form.on_antithyroid_medication.data], 
                                        sick_patient_reports_malaise = conversion_boolean[form.sick_patient_reports_malaise.data], 
                                        pregnant = conversion_boolean[form.pregnant.data], 
                                        thyroid_surgery = conversion_boolean[form.thyroid_surgery.data],
                                        treatment = conversion_boolean[form.treatment.data],
                                        test_hypothyroid = conversion_boolean[form.test_hypothyroid.data],
                                        test_hyperthyroid = conversion_boolean[form.test_hyperthyroid.data],
                                        on_lithium = conversion_boolean[form.on_lithium.data], 
                                        has_goitre = conversion_boolean[form.has_goitre.data],
                                        has_tumor = conversion_boolean[form.has_tumor.data],
                                        hypopituitary = conversion_boolean[form.hypopituitary.data], 
                                        psychological_symptoms = conversion_boolean[form.psychological_symptoms.data],
                                        tsh = form.tsh.data,
                                        t_three = form.t_three.data,
                                        tt_four = form.tt_four.data, 
                                        t_four_u = form.t_four_u.data,
                                        fti = form.fti.data, 
                                        access = True,

                                        correct_prediction = None
                                    )

            if not checkFileToPredict('thyroid',MODEL_PATH_THYROID,PATH_THYROID):
                return render_template('info.html',info='Problemy ze spójnością plików')                  
            #Dodanie do bazy danych
            db.session.add(new_patient)


            for param in models_score:
                print(param[0])
                classificator = Algoritm.query.filter_by(model = param[0], type='thyroid',access=True).first()
                new_alg = Algoritm_PatientThyroid(patient = new_patient,
                                            algoritmThyroid = classificator,
                                            prediction =param[1])
                db.session.add(new_alg)
            db.session.commit()


            return render_template('form_predict/predict_result.html', models_score = models_score)
        return render_template('form_predict/form_predict_Thyroid.html',form=form)
    except Exception as e:
        print(f'Error: {e}')
        db.session.rollback()
        return render_template('info.html',info = e)


@patientThyroidController.route('/table/thyroid', methods=['GET','POST'])
def table():
    '''
    Wypisywanie listy pacjentów, wraz z możliwością
    filtrowania danych pod kątem wyników predykcji
    wykonanych przez algorytmy
    '''
    try:
        if request.method == 'GET':
            #Wykonywanie dla GET
            patient_list = Patientthyroid.query.filter_by(access=True).all()
            return render_template('patient_list/table_Thyroid.html', patient_list = patient_list)
        else: 
            #POST
            filtr_table = request.form['filtr']
            patient_list = Patientthyroid.query.filter_by(access=True).all()
            print(patient_list)
            correct_patient_list = controllerservice.filtr_table(filtr_table, patient_list)

            return render_template('patient_list/table_Thyroid.html', patient_list = correct_patient_list)
    except Exception as e:
        print(e)
        return render_template('error.html')

@patientThyroidController.route('/table/atrchivesThyroid', methods=['GET','POST'])
def atrchives_table():
    try:
        distinctValue = db.session.query(Algoritm.version).filter_by(type='thyroid',access=False).join(Algoritm_PatientThyroid).filter_by(algorytmML_id = Algoritm.id).distinct()
        list_version = [nrVersion[0] for nrVersion in distinctValue] 
        list_version.append('all')
        if request.method == 'GET':
            #Wykonywanie dla GET
            patient_list = Patientthyroid.query.filter_by(access=False).all()
            return render_template('patient_list/atrchivestablethyroid.html', patient_list = patient_list,listVersion = list_version)
        else: 
            #POST
            filtr_table = request.form['filtr']
            version = request.form['version']
            if version != 'all':
                patient_list = Patientthyroid.query.join(Algoritm_PatientThyroid).join(Algoritm).filter_by(version=version)
            else:
                patient_list = Patientthyroid.query.filter_by(access=False).all()
            correct_patient_list = controllerservice.filtr_table(filtr_table, patient_list)

            return render_template('patient_list/atrchivestablethyroid.html',  patient_list = correct_patient_list,listVersion = list_version ) 
    except Exception as e:
        print(f'{e}')
        return render_template('error.html')

@patientThyroidController.route('/delete_patient_Thyroid/<int:patient_id>')
def delete_patient(patient_id):
    '''
    Usuwanie rekordu z bazy danych
    o określonym id
    '''
    try:
        patient = Patientthyroid.query.filter_by(id=patient_id).first()
        db.session.delete(patient)
        db.session.commit()

        return render_template('patient_list/delete_patient.html')     
    except:
        return render_template('error.html')


@patientThyroidController.route('/update_patient_Thyroid/<int:patient_id>/<int:predict>')
def update_patient(patient_id,predict):
    try:       
        correct_predict = bool(predict)

        patient = Patientthyroid.query.filter_by(id=patient_id).first()
        patient.correct_prediction = correct_predict
        db.session.commit()
        return redirect(url_for('patientThyroidController.table'))
    except:
        return render_template('error.html')  