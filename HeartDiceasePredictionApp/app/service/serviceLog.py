import os.path, time
import pandas as pd
from os.path import isfile, join
from os import listdir
import shutil

#### METODY DO ZAPISÓW LOG
def saveLog(kind_algoritm,mypath, information_path): 
    path = f"app/log/{kind_algoritm}"
    path_models = [ (f,join(mypath,f)) for f in listdir(mypath) if isfile(join(mypath, f))]
    if os.path.exists(path):
        print('Istnieje')
        shutil.rmtree(path)

    os.makedirs(path)

    file = open(f"{path}/logAlgoritm.txt",'w')
    for j,i in path_models:
        file.write(f" {j} Last modified:  {time.ctime(os.path.getmtime(i))}\n")
    file.close()

    file = open(f"{path}/logInfo.txt",'w')
    file.write(f"Last modified:  {time.ctime(os.path.getmtime(information_path))}\n")
    file.close()

### SPRAWDZANIE ZMIAN
def checkAlgoritmLog(kind_algoritm,mypath):
    ##Porównanie ilości algorytmów z ilością logów
    log_file_algoritm = open(f"app/log/{kind_algoritm}/logAlgoritm.txt",'r')
    count_save_log = 0
    modifeLog = ''
    for line in log_file_algoritm:
        count_save_log += 1
        modifeLog += line

    current_algoritm=[(f,join(mypath,f)) for f in listdir(mypath) if isfile(join(mypath, f))]
    count_current_algoritm = len(current_algoritm)

    if count_current_algoritm != count_save_log:
        return True

    ## Sprawdzenie czy są różnice między logami a plikami
    modifeCurrent =''
    for j,i in current_algoritm:
        modifeCurrent += f" {j} Last modified:  {time.ctime(os.path.getmtime(i))}\n"

    log_file_algoritm.close()
    if modifeCurrent != modifeLog:
        return True

    return False

##Ilość algorytmów a ilość informacji 
def checkLogInfoFile(kind_algoritm,mypath, information_path):
    try:
        count_current_algoritm=len([(f,join(mypath,f)) for f in listdir(mypath) if isfile(join(mypath, f))])
        file_information = open(information_path,'r')
        size = len([line for line in file_information])-1 #Usuwanie z obliczeń kolumny
        if size != count_current_algoritm: return None
        file_information.close()

        ##Sprawdzenie logów plików informacyjnych
        curent_modieInfo = f'Last modified:  {time.ctime(os.path.getmtime(information_path))}\n'
        log_file_info = open(f'app/log/{kind_algoritm}/logInfo.txt','r')
        log_modifeInfo = ''
        for line in log_file_info:
            log_modifeInfo += line

        return curent_modieInfo != log_modifeInfo
    except :
        return None


def compareContentFile(mypath,information_path):
    '''
    Metoda sprawdzająca czy inforamcajce o algorytmach w pliku
    są spójne z nazwami plików.
    Nazwa pliku musi odpowiadac nazwie zawartym w pliku z opisem
    '''
    try:
        print('Wykonuje się to')
        models = pd.read_csv(information_path).to_dict('list')
        models['model'].sort()
        path_models = [f.replace('.bin','') for f in listdir(mypath) if isfile(join(mypath, f))]
        path_models.sort()
        print(models['model'] == path_models)
        return models['model'] == path_models
    except Exception as e:
        print(f'{e}')

def checkFileToUpdate(kind_algoritm,mypath, information_path):
    print('Test działa')
    if not compareContentFile(mypath, information_path): 
        print('zła ilość')
        return False
    if checkAlgoritmLog(kind_algoritm,mypath):
        #Algorytmy się różnią
        print('Algorytmy się zmieniły')
        return checkLogInfoFile(kind_algoritm,mypath, information_path) # jeśli true to aktualizuje
    else:
        print('Algorytmy się nie zmieniły')
        return False

def checkFileToPredict(kind_algoritm,mypath, information_path):
    try:     
        if not print(checkAlgoritmLog(kind_algoritm,mypath)):
            result = checkLogInfoFile(kind_algoritm,mypath, information_path)
            print(result)
            if result == None:
                return False
            else:
                return not result
        else:
            return False
    except Exception as e:
        print(f'Error {e}')
