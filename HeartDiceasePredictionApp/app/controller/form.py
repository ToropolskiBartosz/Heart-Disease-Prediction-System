from flask import Blueprint, render_template

form = Blueprint('form',__name__)


@form.route('/form_predict')
def form_predict():
    return render_template('form_predict/form_predict.html')