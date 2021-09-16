from flask import Blueprint, render_template, request
from app import db
import pandas as pd
import pickle
from os import listdir
from os.path import isfile, join
from app.models.patient import Patient

form = Blueprint('form',__name__)

mypath = '../Models_ML/models/'
path_models = [(f, join(mypath, f)) for f in listdir(mypath) if isfile(join(mypath, f))]

models = {}
for name_model, model in path_models:
    with open(model, 'rb') as f_in:
        short_name_model = name_model.replace('.bin','')
        models[short_name_model] = pickle.load(f_in)

@form.route('/form_predict')
def form_predict():
    return render_template('form_predict/form_predict.html')


@form.route('/predict', methods=['POST'])
def send(sum=sum):
    if request.method == 'POST':
        patient_data = request.form

        df = preprocesing_data(patient_data)
        models_score = []
        p = {0: False, 1: True}
        
        #Predict Dicease
        for model in models.keys():
            score = models[model].predict(df)[0]
            models_score.append((model, p[score]))

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
        db.session.add(new_patient)
        db.session.commit()
        
    return render_template('form_predict/predict_result.html', models_score = models_score)



def preprocesing_data(patient_data):
    '''
    :patient_data: tablica zawierająca dane z formularzu

    funkcja odpowiadajaca za przygotowanie
    danych pobranych metodą POST z formularza
    do załadowania modelów ML w celu predykcji
    zagrożenia chorobą serva
    '''

    patient_dic = {}
    correct_order = ['age', 'sex', 'cp', 
            'trestbps', 'chol', 'fbs',
            'restecg', 'thalach', 'exang', 
            'oldpeak', 'slope', 'ca',
            'thal']

    for name_parametr in correct_order:
        patient_dic[name_parametr] = patient_data[name_parametr]

    df = pd.DataFrame(data=patient_dic, index=[0])
    cat_col = ['sex','cp','fbs','restecg','exang','slope','thal']
    num_col = ['age', 'trestbps', 'chol',  'thalach',  'oldpeak','ca']

    for col in cat_col:
        df[col] = df[col].astype('object')
    for col in num_col:
        df[col] = df[col].astype('float64')
      
    return df
    