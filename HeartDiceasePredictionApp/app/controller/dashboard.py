from flask import Blueprint, render_template, request
import pandas as pd

dash = Blueprint('dash',__name__)


@dash.route('/dashboard')
def dashboard():
    '''
    Wybisywanie informacji takich jak:
    dokładność, precyzja, czułość, f1, AUC i wartość stary
    o wszystkich algorytmach wykorzystywanych w aplikacji
    '''
    try:
        models = pd.read_csv('../Models_ML/infomodels/infoModels.csv')
        models = models.round(3)
        
        model_info = models.to_dict('list')
        list_info = ['model','test_score','precision','recall','f1','AUC','cost_of_loss']
        len_info = len(model_info['model'])

        return render_template('dash.html', model_info = model_info, list_info = list_info, len_info = len_info)
    except:
        return render_template('error.html')