# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 08:56:45 2019

@author: savio.pereira
"""

from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import numpy as np

class getIPEA:
    '''
    Classe responsável por coletar os dados do IPEA
    '''
    def __init__(self, directory, link='http://www.ipeadata.gov.br/api/odata4/Metadados', allTable=False):
        '''
        Classe de parâmetros iniciais;
        directory = diretório para salvar planilhas
        link = link do site do IPEA
        allTable = Coletar todas as tabelas; opcão inicial é "False"
        '''
        self.directory = directory
        self.link = link
        self.allTable = allTable
        
    def initialScraping(self):
        '''
        Inicia a raspagem das informações primárias para acesso da API do IPEA
        '''        
        #Solicitando resposta
        answer = requests.get(self.link) 
        
        #Armazenando os dados iniciais
        data = json.loads(str(answer.text))
        
        #Criando DataFrame
        initialDF = pd.DataFrame(data['value'])
        
        return initialDF
    
    def availableFont(self):
        '''Disponibilizando as fontes dos dados'''
        
        #Chamando a função initialScraping
        initialDF = self.initialScraping()
        
        #Armazenando todas as fontes
        initialsFont = np.unique(np.asrray(initialDF['FNTSIGLA'].values))
        
        return initialsFont
    
    def availableTable(self, font):
        '''
        Disponibilizando todas as tabelas da fonte escolhida
        font = Selecionar a partir das opções mostradas por availableFont
        '''
        
        #Decisão: se opção for por todas as tabelas, então ele passa direto nesta função
        if self.allTable == True:
            pass
        else:
            #Chamando a função initialScraping
            initialDF = self.initialScraping()
            
            #Pegando todas as informações
            initialFont = np.asarray(initialDF['FNTSIGLA'].values) 
            
            index = []
            for sig in range(len(initialFont)):
                if font == initialFont[sig]:
                    index.append(sig)
                    
            initialSubject = np.asarray(initialDF['SERNOME'].values)
            
            availableTable = []
            for i in range(len(initialSubject)):
                for j in index:
                    if i == j:
                        availableTable.append(initialSubject[i])
                        
            return availableTable
        
    def scrapingTable(self, table):
        '''
        Função de raspagem de uma tabela do IPEA
        table: Nome da tabela; Olhar os nomes das tabelas conforme a fonte
        na função availableTable
        '''
        initialDF = self.initialScraping()
        
        for i, j in zip(np.asarray(initialDF['SERCODIGO'].values), np.asarray(initialDF['SERNOME'].values)):
            if j == table:
                cod_table = str(i)
        self.link = self.link + "('%s')/Valores"%cod_table
        
        #Solicitando resposta
        answer = requests.get(self.link) 
        
        #Armazenando os dados iniciais
        data = json.loads(str(answer.text))
        
        #Criando DataFrame
        df = pd.DataFrame(data['value'])
        
        df.to_excel(self.directory + '%s.xlsx'%cod_table, index_label = None,
                    encoding = 'utf-8', engine = 'openpyxl')