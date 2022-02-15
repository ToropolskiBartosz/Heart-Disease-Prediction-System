from os import access, path
from flask_sqlalchemy import model
import pandas as pd
from app.models.patient import Algoritm,Patient,Patientbreastcancer,Patientthyroid
from app import db
from app.service.serviceLog import saveLog,checkFileToUpdate,compareContentFile

PATH_BREASTCANCER = './Models_ML/infomodels/breastCancer.csv'
PATH_THYROID = './Models_ML/infomodels/thyroid.csv'
PATH_HEARTDICEASE = './Models_ML/infomodels/heartdisease.csv'

MODEL_PATH = './Models_ML/models/heartdisease'
MODEL_PATH_BREASTCANCER = './Models_ML/models/breastCancer'
MODEL_PATH_THYROID = './Models_ML/models/thyroid'

#BREASTCANCER = pd.read_csv(PATH_BREASTCANCER)
#THYROID = pd.read_csv(PATH_THYROID)
#HEARTDICEASE = pd.read_csv(PATH_HEARTDICEASE)

def addAlgoritms(app):
    try:   
        if path.exists('app/log'): raise Exception('Error data already load') 
        _createAllLog()
        if (not compareContentFile(MODEL_PATH,PATH_HEARTDICEASE)
            and not compareContentFile(MODEL_PATH_BREASTCANCER,PATH_BREASTCANCER)
            and not compareContentFile(MODEL_PATH_THYROID,PATH_THYROID)):
            raise Exception('Error during load content db')

        modelsbreastcancer = pd.read_csv(PATH_BREASTCANCER)
        modelsthyroid = pd.read_csv(PATH_THYROID)
        models = pd.read_csv(PATH_HEARTDICEASE)
        modelsbreastcancer = modelsbreastcancer.round(3)
        modelsthyroid = modelsthyroid.round(4)
        models = models.round(3)
                
        information_modelsBreastcancer = extract_information(modelsbreastcancer)
        information_modelsThyroid = extract_information(modelsthyroid)
        information_modelsHeard = extract_information(models)

        modelsbreastcancer_info = information_modelsBreastcancer['model_info']
        modelsthyroid_info = information_modelsThyroid['model_info']
        model_heartdicease_info = information_modelsHeard['model_info']

        len_info_bc = information_modelsBreastcancer['len_info']
        len_info_t = information_modelsThyroid['len_info']
        len_info_hd = information_modelsHeard['len_info']

        list_model_info = [(len_info_hd,model_heartdicease_info,'heartdicease')
                            ,(len_info_bc,modelsbreastcancer_info,'breastcancer')
                            ,(len_info_t,modelsthyroid_info,'thyroid')]


        with app.app_context():
            for len,model_info,type_model in list_model_info:
                for index_algoritm in range(0,len):
                    new_algorimt = Algoritm(
                                        model=model_info['model'][index_algoritm],
                                        test_score=model_info['test_score'][index_algoritm],
                                        precision=model_info['precision'][index_algoritm], 
                                        recall=model_info['recall'][index_algoritm], 
                                        f1=model_info['f1'][index_algoritm], 
                                        auc=model_info['AUC'][index_algoritm], 
                                        cost_of_loss= model_info['cost_of_loss'][index_algoritm],
                                        type = type_model,
                                        access = True,
                                        version = 1
                                        )

                                
                    db.session.add(new_algorimt)
            db.session.commit()
    except Exception as e:
        with app.app_context():
            db.session.rollback()
            print(f'To sie stalo: {e}')


def updateAlgoritmsHeartdicease():
    try:
        if not checkFileToUpdate('heartdicease',MODEL_PATH,PATH_HEARTDICEASE):
            return False
        type_algoritm = 'heartdicease'
        models = pd.read_csv(PATH_HEARTDICEASE)  
        models = models.round(3)
        information_models = extract_information(models)
        model_info = information_models['model_info']
        len_info = information_models['len_info']
        _updateAlgoritms(model_info, len_info, type_algoritm)
        patient = Patient.query.filter_by(access=True)
        for p in patient: p.access = False
        db.session.commit()
        saveLog('heartdicease',MODEL_PATH,PATH_HEARTDICEASE)
        return True
    except:
        db.session.rollback
        return False

def updateAlgoritmsBreastcancer():
    try:
        if not checkFileToUpdate('breastcancer',MODEL_PATH_BREASTCANCER,PATH_BREASTCANCER):
            return False
        type_algoritm = 'breastcancer'
        models = pd.read_csv(PATH_BREASTCANCER)
        models = models.round(3)
        information_models = extract_information(models)
        model_info = information_models['model_info']
        len_info = information_models['len_info']
        _updateAlgoritms(model_info, len_info, type_algoritm)
        patient = Patientbreastcancer.query.filter_by(access=True)
        for p in patient: p.access = False
        db.session.commit()
        saveLog('breastcancer',MODEL_PATH_BREASTCANCER,PATH_BREASTCANCER)
        return True
    except:
        db.session.rollback
        return False

def updateAlgoritmsThyroid(): 
    try: 
        if not checkFileToUpdate('thyroid',MODEL_PATH_THYROID,PATH_THYROID):
            return False
        type_algoritm = 'thyroid'
        models = pd.read_csv(PATH_THYROID)
        models = models.round(3)
        information_models = extract_information(models)
        model_info = information_models['model_info']
        len_info = information_models['len_info']
        _updateAlgoritms(model_info, len_info, type_algoritm)
        patient = Patientthyroid.query.filter_by(access=True)
        for p in patient: p.access = False
        db.session.commit()
        saveLog('thyroid',MODEL_PATH_THYROID,PATH_THYROID)
        return True
    except:
        db.session.rollback
        return False

def _updateAlgoritms(model_info, len_info, type_algoritm):
    try:
        version = Algoritm.query.filter_by(type=type_algoritm,access=True).first()
        nrVersion = 0
        if version == None: 
            nrVersion = 1
        else:
            nrVersion = version.version + 1

        algorimt = Algoritm.query.filter_by(type=type_algoritm,access=True).all()
        for a in algorimt: a.access = False
        for index_algoritm in range(0,len_info):
            new_algorimt = Algoritm(
                            model=model_info['model'][index_algoritm],
                            test_score=model_info['test_score'][index_algoritm],
                            precision=model_info['precision'][index_algoritm], 
                            recall=model_info['recall'][index_algoritm], 
                            f1=model_info['f1'][index_algoritm], 
                            auc=model_info['AUC'][index_algoritm], 
                            cost_of_loss= model_info['cost_of_loss'][index_algoritm],
                            type = type_algoritm,
                            access = True,
                            version = nrVersion
                                    )
            #algorimt = Algoritm.query.filter_by(model=model_info['model'][index_algoritm],type=type_algoritm,access=True).first()
            #if algorimt !=None: algorimt.access = False
            db.session.add(new_algorimt)
        db.session.commit()
    except:
        db.session.rollback

def _createAllLog():
    print('Robimy logi')
    saveLog('heartdicease',MODEL_PATH,PATH_HEARTDICEASE)
    saveLog('breastcancer',MODEL_PATH_BREASTCANCER,PATH_BREASTCANCER)
    saveLog('thyroid',MODEL_PATH_THYROID,PATH_THYROID)


def extract_information(df):
    model_info = df.to_dict('list')
    list_info = ['model','test_score','precision','recall','f1','AUC','cost_of_loss']
    len_info = len(model_info['model'])
    all_info = {'model_info':model_info,'list_info':list_info,'len_info':len_info}
    return all_info 


