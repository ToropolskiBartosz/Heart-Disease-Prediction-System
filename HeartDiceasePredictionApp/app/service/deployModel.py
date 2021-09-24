import pickle
from os.path import isfile, join
from os import listdir

def deploy_model(mypath):
    '''
    :mypath: zmienna zawierająca ścieżkę do modeli zapisanych 
             z rozszerzeniem .bin

    :models: słownik zawierający nazwę modelu oraz model

    Funkcja odpowiadająca do zaimplementowania
    algorymów 
    '''
    #Scieżka do modeli
    path_models = [(f, join(mypath, f)) for f in listdir(mypath) if isfile(join(mypath, f))]

    models = {}
    #Odczytywanie modeli
    for name_model, model in path_models:
        with open(model, 'rb') as f_in:
            short_name_model = name_model.replace('.bin','')
            models[short_name_model] = pickle.load(f_in)

    return models