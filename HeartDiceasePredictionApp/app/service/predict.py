from app.service.deployModel import deploy_model
import pandas as pd

MODEL_PATH = '../Models_ML/models/'

models = deploy_model(MODEL_PATH)

def preprocesing_data(patient_data):
    '''
    :patient_data: tablica zawierająca dane z formularzu
    
    :df: obiekt datafrem zawierający dane pacjenta

    funkcja odpowiadajaca za przygotowanie
    danych pobranych metodą POST z formularza
    do załadowania modelów ML w celu predykcji
    zagrożenia chorobą serva
    '''

    patient_dic = {}
    correct_order = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs',
                    'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca','thal']

    #Ułożenie danych w odpowiedniej kolejności
    for name_parametr in correct_order:
        patient_dic[name_parametr] = patient_data[name_parametr]

    df = pd.DataFrame(data=patient_dic, index=[0])
    cat_col = ['sex','cp','fbs','restecg','exang','slope','thal']
    num_col = ['age', 'trestbps', 'chol',  'thalach',  'oldpeak','ca']

    #Konwertowanie typów
    for col in cat_col:
        df[col] = df[col].astype('object')
    for col in num_col:
        df[col] = df[col].astype('float64')
      
    return df


def predict_dicease(patient_data):
    '''
    :patient_data: dane pacjenta na bazie, których 
                   zostaje wykonana predykcja zagrożenia

    :models_score: słownik z wynikami predykcji

    Funkcja ta odpowiada, za wykonanie przez wszystkie
    algorytmy sztucznej inteligencji predykcji zagrożenia
    horobą i następnie zapisanie wyników do słownika
    '''
    #Przekształcenie danych
    df = preprocesing_data(patient_data)
    models_score = []
    p = {0: False, 1: True}
            
    #Predict Dicease
    for model in models.keys():
        score = models[model].predict(df)[0]
        models_score.append((model, p[score]))
    
    return models_score
