from os import access,listdir
from app import db
from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy.orm import session
from app.service import dashservice 
import pandas as pd
from app.models.patient import Algoritm,Algoritm_Patient,Algoritm_PatientThyroid,Algoritm_PatientBreastCancer
from flask import Flask


dash = Blueprint('dash',__name__)


@dash.route('/dashboard')
def dashboard():
    '''
    Wybisywanie informacji takich jak:
    dokładność, precyzja, czułość, f1, AUC i wartość stary
    o wszystkich algorytmach wykorzystywanych w aplikacji
    '''
    return render_template('dashbords/dashmain.html')

@dash.route('/dashboard/dash/infoModels')
def dashboard_heartdisease():
    '''
    Wybisywanie informacji takich jak:
    dokładność, precyzja, czułość, f1, AUC i wartość stary
    o wszystkich algorytmach wykorzystywanych w aplikacji
    '''
    try:       
        algoritm_list = Algoritm.query.filter_by(type='heartdicease',access=True).all()

        return render_template('dashbords/dash.html', algoritm_list = algoritm_list, algoritm = 'heartdisease')
    except Exception as e:
        print(e)
        return render_template('error.html')

@dash.route('/dashboard/dash/infoModels_BreastCancer')
def dashboard_BreastCancer():
    '''
    Wybisywanie informacji takich jak:
    dokładność, precyzja, czułość, f1, AUC i wartość stary
    o wszystkich algorytmach wykorzystywanych w aplikacji
    '''
    try:
        algoritm_list = Algoritm.query.filter_by(type='breastcancer',access=True).all()

        return render_template('dashbords/dash.html', algoritm_list = algoritm_list, algoritm = 'breastcancer')
    except:
        return render_template('error.html')

@dash.route('/dashboard/dash/infoModels_Thyroid')
def dashboard_Thyroid():
    '''
    Wybisywanie informacji takich jak:
    dokładność, precyzja, czułość, f1, AUC i wartość stary
    o wszystkich algorytmach wykorzystywanych w aplikacji
    '''
    try:
        algoritm_list = Algoritm.query.filter_by(type='thyroid',access=True).all()

        return render_template('dashbords/dash.html', algoritm_list = algoritm_list, algoritm = 'thyroid')
    except:
        return render_template('error.html')



@dash.route('/dashboard/dash/Dash')
def dashboard_compare():
    '''
    Wybisywanie informacji takich jak:
    dokładność, precyzja, czułość, f1, AUC i wartość stary
    o wszystkich algorytmach wykorzystywanych w aplikacji
    '''
    try:
        algoritm_list = Algoritm.query.filter_by(access=True).all()
        print(algoritm_list)
        algoritm_list = list(set(map(lambda x: x.model, algoritm_list)))
        algoritm_list.sort()
        list_algoritm_info = []
        list_algoritm_info = dashservice.algoritmResult(algoritm_list)
        return render_template('dashbords/dashcompare.html', algoritm_list = list_algoritm_info)
    except Exception as e:
        print(e)
        return render_template('error.html')

@dash.route('/dashboard/dash/archives')
def archives():
    return render_template('dashbords/archivesmain.html')

@dash.route('/dashboard/archives/infoModels', methods=['GET','POST'])
def archives_heartdisease():
    try:     
        distinctValue = db.session.query(Algoritm.version).filter_by(type='heartdicease',access=False).join(Algoritm_Patient).filter_by(algorytmML_id = Algoritm.id).distinct()
        list_version = [nrVersion[0] for nrVersion in distinctValue]
        if request.method == 'GET':  
            algoritm_list = Algoritm.query.filter_by(type='heartdicease',access=False).all()    
            
            return render_template('dashbords/archivesdash.html', 
            algoritm_list = algoritm_list, 
            algoritm = 'heartdisease',
            listVersion = list_version)
        else:
            filtr = request.form['filtr']
            algoritm_list = Algoritm.query.filter_by(version=int(filtr),type='heartdicease').all()
           
            return render_template('dashbords/archivesdash.html', 
            algoritm_list = algoritm_list, 
            algoritm = 'heartdisease',
            listVersion = list_version,
            version = filtr)
    except Exception as e:
        print(e)
        return render_template('error.html')

@dash.route('/dashboard/archives/infoModels_BreastCancer', methods=['GET','POST'])
def archives_breastcancer():
    try:    
        distinctValue = db.session.query(Algoritm.version).filter_by(type='breastcancer',access=False).join(Algoritm_PatientBreastCancer).filter_by(algorytmML_id = Algoritm.id).distinct()
        list_version = [nrVersion[0] for nrVersion in distinctValue] 
        if request.method == 'GET':  
            algoritm_list = Algoritm.query.filter_by(type='breastcancer',access=False).all()
           
            return render_template('dashbords/archivesdashbreastcancer.html', 
            algoritm_list = algoritm_list, 
            algoritm = 'breastcancer',
            listVersion = list_version)
        else:
            filtr = request.form['filtr']
            algoritm_list = Algoritm.query.filter_by(version=int(filtr),type='breastcancer').all()
           
            return render_template('dashbords/archivesdashbreastcancer.html', 
            algoritm_list = algoritm_list, 
            algoritm = 'breastcancer',
            listVersion = list_version,
            version = filtr)
    except Exception as e:
        print(e)
        return render_template('error.html')

@dash.route('/dashboard/archives/infoModels_Thyroid', methods=['GET','POST'])
def archives_thyroid():
    try:    
        distinctValue = db.session.query(Algoritm.version).filter_by(type='thyroid',access=False).join(Algoritm_PatientThyroid).filter_by(algorytmML_id = Algoritm.id).distinct()
        list_version = [nrVersion[0] for nrVersion in distinctValue] 
        if request.method == 'GET':  
            algoritm_list = Algoritm.query.filter_by(type='thyroid',access=False).all()
           
            return render_template('dashbords/archivesdashthyroid.html', 
            algoritm_list = algoritm_list, 
            algoritm = 'thyroid',
            listVersion = list_version)
        else:
            filtr = request.form['filtr']
            algoritm_list = Algoritm.query.filter_by(version=int(filtr),type='thyroid').all()
            
            return render_template('dashbords/archivesdashthyroid.html', 
            algoritm_list = algoritm_list, 
            algoritm = 'thyroid',
            listVersion = list_version,
            version = filtr)
    except Exception as e:
        print(e)
        return render_template('error.html')

@dash.route('/dashboard/upload', methods=['GET','POST'])
def uploadData():
    if request.method == 'GET':
        return render_template('dashbords/uploadform.html')
    else:
        info = request.files['info']
        algoritms = request.files.getlist('algoritms')
        message = dashservice.uploadFile(info,algoritms)
        return render_template('dashbords/uploadform.html',message=message)

def extract_information(df):
    model_info = df.to_dict('list')
    list_info = ['model','test_score','precision','recall','f1','AUC','cost_of_loss']
    len_info = len(model_info['model'])
    all_info = {'model_info':model_info,'list_info':list_info,'len_info':len_info}
    return all_info 


