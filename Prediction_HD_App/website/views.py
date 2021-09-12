from flask import (
    Flask, 
    render_template, 
    request,
    Blueprint)

view = Blueprint('view', __name__)

@view.route('/')
def main():
    return render_template('index.html')

@view.route('/form_predict')
def form_predict():
    return render_template('form_predict.html')