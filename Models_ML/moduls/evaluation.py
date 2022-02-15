from sklearn.metrics import (
                accuracy_score,
                roc_auc_score,
                recall_score,
                precision_score,
                f1_score
)

def cost_of_loss(label, predict_label):
    '''
    :label: orginalne dane
    :predict_label: przewidywane wartości
    
    Metoda służąca do 
    obliczenia kosztów straty 
    '''
    price = 0
    for index in range(0, len(predict_label)):
        if predict_label[index] == 0 and predict_label[index] != label.iloc[index]:
            price += 5
        elif predict_label[index] == 1 and predict_label[index] != label.iloc[index]:
            price += 1
            
    return price

def describe_model(label, predict_label,predict_proba):
    '''
    :label: orginalne dane
    :predict_label: przewidywane wartości
    
    :return: słownik z wartościmi poszczególnych miar
    Metoda służąca do 
    wyliczenie różnych miar służących
    do określenia ewaluacji modelu
    '''
    dic = {}
    dic['test_score'] = accuracy_score(label, predict_label)#acc
    dic['recall'] = recall_score(label, predict_label, average=None)[1]#czułość
    dic['precision'] = precision_score(label, predict_label)
    dic['f1'] = f1_score(label, predict_label, average=None)[1]
    dic['auc'] = roc_auc_score(label, predict_proba)#Pole powierzchni pod krzywą ROC
    dic['cost_of_loss'] = cost_of_loss(label, predict_label)
    
    return dic