
def filtr_table(filtr_table, patient_list):
    '''
    :filtr_table: atrybut określający warunek logiczny
    :patient_list: lista z obiektami wyświetlanymi w tabeli
    Metoda odpowiadająca za filtrowanie tabeli.
    :return correct_patient_list: lista z przefiltrowanymi obiektamis
    '''
    correct_patient_list = []
    if filtr_table == 'all':
        #Wypisanie wszystkich rekordów              
        return patient_list

    elif filtr_table == 'allr':
        #Wypisanie rekordów bez prawdopodobieństwa zagrożenia             
        for patient in patient_list:
            if all(map(lambda x: not x.prediction ,patient.patient_algoritmML_id)) : 
                correct_patient_list.append(patient)

        return correct_patient_list

    elif filtr_table == 'dan':
        #Wypisanie rekordów gdzie istnieje jakieś zagrożenie
        #Przynajmnie jedna pozytywna predykcja przewidziana przez algorytm 
        for patient in patient_list:
            if all(map(lambda x: x.prediction ,patient.patient_algoritmML_id)) : 
                correct_patient_list.append(patient)

        return correct_patient_list

    else:
        #Wypisywanie wszystkich rekordów z niebezpeczeństem
        #Wszystkie predykcjie były pozytywne
        for patient in patient_list:
            if (any(map(lambda x: x.prediction ,patient.patient_algoritmML_id))
                and not all(map(lambda x: x.prediction ,patient.patient_algoritmML_id))): 
                correct_patient_list.append(patient)

        return correct_patient_list

