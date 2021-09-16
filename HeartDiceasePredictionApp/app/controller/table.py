from operator import or_
from flask import Blueprint, render_template, request
from app.models.patient import Patient
from sqlalchemy import or_
from app import db

table = Blueprint('table',__name__)

@table.route('/table', methods=['GET','POST'])
def form_predict():
    if request.method == 'GET':
        patient_list = Patient.query.all()
        return render_template('patient_list/table.html', patient_list = patient_list)

    else: #POST
        filtr_table = request.form['filtr']

        if filtr_table == 'all':
            patient_list = Patient.query.all()
            return render_template('patient_list/table.html', patient_list = patient_list)

        elif filtr_table == 'allr':
            patient_list = Patient.query.filter_by(decisiontree = False,
                                                    knn = False,
                                                    logisticregression = False,
                                                    mlp = False,
                                                    randomforest =False,
                                                    scv = False)

            return render_template('patient_list/table.html', patient_list = patient_list)

        elif filtr_table == 'dan':
            patient_list = Patient.query.filter_by(decisiontree = True,
                                                    knn = True,
                                                    logisticregression = True,
                                                    mlp = True,
                                                    randomforest =True,
                                                    scv = True)
            return render_template('patient_list/table.html', patient_list = patient_list) 

        else:
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



@table.route('/delete_patient/<int:patient_id>')
def view_table(patient_id):

    patient = Patient.query.filter_by(id=patient_id).first()
    db.session.delete(patient)
    db.session.commit()

    return render_template('patient_list/delete_patient.html')