import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class DataMenager:   
    def __init__(self, data_path, data_url=None):
        self.data_path = data_path
        self.data_url = data_url
        
    def fetch_data_from_web(self, name_data, sep=','):
        '''
        Metoda odpowiadająca za pobranie zbioru danych
        z repozytorum universytetu calofornijeskego
        '''
        try:
            if not os.path.isdir(self.data_path + '/raw'):
                os.makedirs(self.data_path + '/raw')
            df = pd.read_csv(self.data_url, header = None, sep=sep)    
            df.to_csv(f'{self.data_path}/raw/{name_data}',index=False)
        except:
            print('Error')
            
    def load_raw_data(self, name_data, columns=None, sep=','):
        try:
            df = pd.read_csv(f'{self.data_path}/raw/{name_data}', sep=sep)
            if columns:
                df.columns = columns
            return df
        except:
            print('Dane nie mogły zostac załadowane ')
    
    def uploade_data(self, dataframe, name_data):
        '''
        Metoda służąca do szybiekgo zapisania danych
        do katalogu ustawionego przy wywołaniu klasy '''
        try:
            if not os.path.isdir(self.data_path + '/preprocessing'):
                os.makedirs(self.data_path + '/preprocessing')
                
            dataframe.to_csv(f'{self.data_path}/preprocessing/{name_data}',index=False)
        except:
            print('Dane nie zostały zapisane')    
    
    def load_preprocessing_data(self, name_data, sep=','):
        try:
            df = pd.read_csv(f'{self.data_path}/preprocessing/{name_data}', sep=sep)
            return df
        except:
            print('Dane nie mogły zostac załadowane ')