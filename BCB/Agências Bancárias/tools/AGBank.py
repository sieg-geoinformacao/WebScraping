# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 09:52:18 2019

@author: savio.pereira
"""

from bs4 import BeautifulSoup
import requests
import json
import pandas as pd

#Criando a classe de aquisição de dados sobre agências bancárias. Fonte: Banco Central do Brasil
class getAGBank:
    '''
    Obtém dados sobre agências bancárias
    '''
    def __init__(self, directory,
                 link='https://olinda.bcb.gov.br/olinda/servico/Informes_Agencias/versao/v1/odata/Agencias?$top=100&$format=json'):
        '''
        Parâmetros Iniciais:
        directory = diretório para salvar planilha
        link = link do site
        '''
        self.link = link
        self.directory = directory
        
    def scrapingJson(self):
        '''
        Raspagem da API em formato JSON
        '''
        answer = requests.get(self.link)
        data = json.loads(str(answer.text))
        return data['value']
        
    def scrapingTable(self):
        '''
        Transformando dados obtidos em formato JSON em uma DataFrame
        '''
        data = self.scrapingJson()
        df = pd.DataFrame(data)
        return df
    
    def saveFile(self):
        '''
        Salva o DataFrame obtido no diretório escolhido
        '''
        df = self.scrapingTable()
        df.to_excel(self.directory + 'Agências Bancárias.xlsx', index_label = None,
                    encoding = 'utf-8', engine = 'openpyxl')
        
    def extractionTotalFiles(self):
        '''
        Aciona todas as funções ao mesmo tempo
        '''
        return self.saveFile()