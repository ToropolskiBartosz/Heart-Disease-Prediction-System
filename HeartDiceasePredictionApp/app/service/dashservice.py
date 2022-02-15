from os import access,path,listdir,remove
from app.models.patient import( Algoritm,
                         Algoritm_Patient,
                         Algoritm_PatientBreastCancer,
                         Algoritm_PatientThyroid)
from app.service.serviceLog import compareContentFile
from app.service.addAlgoritm import updateAlgoritmsBreastcancer,updateAlgoritmsHeartdicease,updateAlgoritmsThyroid

class PatientData:
    name_model = None
    heartdicease = None
    samples_heartdicease = None
    breastcancer = None
    samples_breastcancer = None
    thyroid = None
    samples_thyroid = None

def getInfo(algoritm):
    '''
    Metoda odpowiadająca za posyskanie
    informaci o wydajności modelu podczas
    klasyfikacji obiektów w aplikacji.
    '''
    #Funkcja pełniąca role nie brania pod uwage wyników predykcji dla usuniętych elementów
    number_prediction = len(list(filter(lambda x: x !=None and x.correct_prediction != None,(list(map(lambda x: x.patient, algoritm))))))    
    count_correct_prediction = 0
    for patien in algoritm:
        if patien.patient != None:
            count_correct_prediction += 1 if patien.patient.correct_prediction == patien.prediction else 0

    acc = round(count_correct_prediction/number_prediction*100,2) if number_prediction !=0 else 0
    return number_prediction, acc

def algoritmResult(algoritm_list):
    list_algoritm_info = []

    for algoritm in algoritm_list:
        algoritm_info = PatientData()
        algoritm_info.name_model = algoritm
        # Pobieranie id poszczególnych algorytmów
        heartdiceaseAlgoritm = Algoritm.query.filter_by(model = algoritm ,type = 'heartdicease',access=True).first()
        breastcancerAlgoritm = Algoritm.query.filter_by(model = algoritm ,type = 'breastcancer',access=True).first()
        thyroidAlgoritm = Algoritm.query.filter_by(model = algoritm ,type = 'thyroid',access=True).first()
        
        #idHeartdiceaseAlgoritm = list(map(lambda x: x.id, heartdiceaseSelectByAlgoritm))
        #idBreastcancerAlgoritm = list(map(lambda x: x.id, breastcancerSelectByAlgoritm))
        #idThyroidAlgoritm = list(map(lambda x: x.id, thyroidSelectByAlgoritm))

        #Pobranie informaci odnoście heardicease
        #target_patient = list(map(lambda x: x.algoritmHeard_patient_id, target))
        if heartdiceaseAlgoritm != None:
            resultHeartdicease = Algoritm_Patient.query.filter_by(algorytmML_id = heartdiceaseAlgoritm.id).all()
            algoritm_info.samples_heartdicease, algoritm_info.heartdicease = getInfo(resultHeartdicease)

        #Pobranie informaci odnoście breastcancer
        if breastcancerAlgoritm != None:
            resultBreastcancer = Algoritm_PatientBreastCancer.query.filter_by(algorytmML_id = breastcancerAlgoritm.id).all()
            print(resultBreastcancer)
            algoritm_info.samples_breastcancer, algoritm_info.breastcancer = getInfo(resultBreastcancer)

        #Pobranie informaci odnoście thyroid
        if thyroidAlgoritm != None:
            resultThyroid = Algoritm_PatientThyroid.query.filter_by(algorytmML_id = thyroidAlgoritm.id).all()
            algoritm_info.samples_thyroid, algoritm_info.thyroid = getInfo(resultThyroid)

        list_algoritm_info.append(algoritm_info)
    
    return list_algoritm_info

def update_algoritm(section):
    try:   
        print(section)
        if section =='heartdisease': 
            result = updateAlgoritmsHeartdicease()
            if result:
                return "udało się"
            else:
                return 'błąd'
        if section =='breastCancer': 
            result = updateAlgoritmsBreastcancer()
            if result:
                return "udało się "
            else:
                return 'błąd'
        if section =='thyroid': 
            result = updateAlgoritmsThyroid()
            if result:
                return "udało się "
            else:
                return 'błąd'
        return 'błąd'

    except Exception as e:
        print(f'{e}')
        return e  

def uploadFile(info,algoritms):
    try:
        dirInfo = './Models_ML/infomodels'
        nameFileInfo = info.filename
        allFileInfo =[f for f in listdir(dirInfo)]
        if not nameFileInfo in allFileInfo:
            message = f'Zla nazwa pliku z informacjami wymagane: {allFileInfo}'
            return message
            
        information_path = path.join(dirInfo,nameFileInfo)
        info.save(information_path)
        count_current_algoritm = len(algoritms)
        file_information = open(information_path,'r')
        size = len([line for line in file_information])-1 #Usuwanie z obliczeń kolumny
        if size != count_current_algoritm:
            message = 'Ilość algorytmów różni się z opisem w pliki .csv'
            return message
        file_information.close()
        nameInfo = nameFileInfo.replace('.csv','')
        dir = f"./Models_ML/models/{nameInfo}"
        for f in listdir(dir):
            remove(path.join(dir, f))
        for filealgoritm in algoritms:
            filealgoritm.save(path.join(dir,filealgoritm.filename))

        message = update_algoritm(nameInfo)
        return message
    except Exception as e:
        message = f"Coś poszło nie tak {e}"
        return message