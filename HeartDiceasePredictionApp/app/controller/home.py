from flask import Blueprint, render_template
from app.models.patient import Patient,Patientthyroid,Patientbreastcancer
main = Blueprint('main',__name__)

@main.route('/')
def test():
    '''
    Główna storna 
    '''
    return render_template('index.html')

@main.route('/form_predict')
def formPredict():
    '''
    Główna storna 
    '''
    return render_template('form_predict/hello_form.html')

@main.route('/table')
def table():
    '''
    Główna storna 
    '''
    total_heard_dicease = Patient.query.filter_by(access=True).count()
    total_breast_cancer = Patientbreastcancer.query.filter_by(access=True).count()
    total_thyroid = Patientthyroid.query.filter_by(access=True).count()
    return render_template('patient_list/hello_table.html',total_heard_dicease = total_heard_dicease,
                                                            total_breast_cancer = total_breast_cancer,
                                                            total_thyroid = total_thyroid )

@main.route('/table/archives')
def archives_table():

    return render_template('patient_list/archivesmain.html')



