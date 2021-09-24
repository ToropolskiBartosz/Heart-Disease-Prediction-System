from flask import Blueprint, render_template

main = Blueprint('main',__name__)

@main.route('/')
def test():
    '''
    Główna storna 
    '''
    return render_template('index.html')



