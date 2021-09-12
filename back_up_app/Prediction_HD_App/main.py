from flask import Flask, render_template, request
import pandas as pd
app = Flask(__name__)

import pickle

with open('../Models_ML/models/DecisionTreeClassifier.bin', 'rb') as f_in:
    model = pickle.load(f_in)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/form_predict')
def form_predict():
    return render_template('form_predict.html')

@app.route('/send', methods=['POST'])
def send(sum=sum):
    if request.method == 'POST':
        patient_data = request.form

        patient_dic = {}
        correct_order = ['age', 'sex', 'cp', 
               'trestbps', 'chol', 'fbs',
               'restecg', 'thalach', 'exang', 
               'oldpeak', 'slope', 'ca',
               'thal']

        for name_parametr in correct_order:
            patient_dic[name_parametr] = patient_data[name_parametr]

        print(patient_dic)
        df = pd.DataFrame(data=patient_dic, index=[0])
        cat_col = ['sex','cp','fbs','restecg','exang','slope','thal']
        num_col = ['age', 'trestbps', 'chol',  'thalach',  'oldpeak','ca']

        for col in cat_col:
            df[col] = df[col].astype('object')
        for col in num_col:
            df[col] = df[col].astype('float64')
      
        print(df)

        score = model.predict(df)[0]
        print(score)
        p = {0:'Nic nie grozi', 1:'Umżesz byczku'}
        print(p[score])
        return render_template('test.html', sum=p[score])


if __name__ == '__main__':
    app.run(debug=True)