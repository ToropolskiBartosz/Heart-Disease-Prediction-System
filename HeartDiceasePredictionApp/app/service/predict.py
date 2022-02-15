from app.service.deployModel import deploy_model
import pandas as pd

MODEL_PATH = './Models_ML/models/heartdisease'
MODEL_PATH_BREASTCANCER = './Models_ML/models/breastCancer'
MODEL_PATH_THYROID = './Models_ML/models/thyroid'



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


def preprocesing_data_breastCancer(patient_data):
    '''
    :patient_data: tablica zawierająca dane z formularzu
    
    :df: obiekt datafrem zawierający dane pacjenta

    funkcja odpowiadajaca za przygotowanie
    danych pobranych metodą POST z formularza
    do załadowania modelów ML w celu predykcji
    zagrożenia chorobą serva
    '''

    patient_dic = {}
    correct_order = ['clump_thickness', 'uniformity_of_cell_size', 'uniformity_of_cell_shape', 'marginal_adhesion', 
           'single_epithelial_cell_size','bare_nuclei', 'bland_chromatin', 'normal_nucleoli', 'mitoses']

    #Ułożenie danych w odpowiedniej kolejności
    for name_parametr in correct_order:
        patient_dic[name_parametr] = patient_data[name_parametr]

    df = pd.DataFrame(data=patient_dic, index=[0])

    #Konwertowanie typów
    for col in correct_order:
        df[col] = df[col].astype('int64')
      
    return df

def preprocesing_data_thyroid(patient_data):
    '''
    :patient_data: tablica zawierająca dane z formularzu
    
    :df: obiekt datafrem zawierający dane pacjenta

    funkcja odpowiadajaca za przygotowanie
    danych pobranych metodą POST z formularza
    do załadowania modelów ML w celu predykcji
    zagrożenia chorobą serva
    '''

    patient_dic = {}
    correct_order = ['age', 'sex', 'on_thyroxine', 
           'maybe_on_thyroxine', 'on_antithyroid_medication', 'sick_patient_reports_malaise',
           'pregnant', 'thyroid_surgery', 'treatment',
           'test_hypothyroid', 'test_hyperthyroid', 'on_lithium',
           'has_goitre','has_tumor','hypopituitary',
           'psychological_symptoms','tsh','t_three',
           'tt_four','t_four_u','fti']

    #Ułożenie danych w odpowiedniej kolejności
    for name_parametr in correct_order:
        patient_dic[name_parametr] = patient_data[name_parametr]

    df = pd.DataFrame(data=patient_dic, index=[0])
    int_col = ['sex', 'on_thyroxine', 'maybe_on_thyroxine', 
                'on_antithyroid_medication', 'sick_patient_reports_malaise','pregnant', 
                'thyroid_surgery', 'treatment','test_hypothyroid', 'test_hyperthyroid', 
                'on_lithium','has_goitre','has_tumor','hypopituitary',
                'psychological_symptoms','age']
    float_col = ['tsh','t_three',
           'tt_four','t_four_u','fti']

    #Konwertowanie typów
    for col in int_col:
        df[col] = df[col].astype('int64')
    for col in float_col:
        df[col] = df[col].astype('float64')
      
    return df


def predict(patient_data,variant):
    '''
    :patient_data: dane pacjenta na bazie, których 
                   zostaje wykonana predykcja zagrożenia

    :models_score: słownik z wynikami predykcji

    Funkcja ta odpowiada, za wykonanie przez wszystkie
    algorytmy sztucznej inteligencji predykcji zagrożenia
    horobą i następnie zapisanie wyników do słownika
    '''
    models_heartdicea = deploy_model(MODEL_PATH)
    models_breastcancer = deploy_model(MODEL_PATH_BREASTCANCER)
    models_thyroid = deploy_model(MODEL_PATH_THYROID)
    #Przekształcenie danych
    if variant == 1:
        df = preprocesing_data(patient_data)
        models = models_heartdicea
    elif variant == 2:
        df = preprocesing_data_breastCancer(patient_data)
        models = models_breastcancer
    elif variant == 3:
        df = preprocesing_data_thyroid(patient_data)
        models = models_thyroid

    models_score = []
    p = {0: False, 1: True}
    
    #Predict Dicease
    for model in models.keys():
        score = models[model].predict(df)[0]
        models_score.append((model, p[score]))


    return models_score


