# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 08:00:42 2019

@author: savio.pereira
"""
#Importando as bibliotecas
from bs4 import BeautifulSoup
import requests
import json
import pandas as pd

#Criando a classe de aquisição de dados do site dados.gov.br
class getGOV:
    '''Aquisição de dados do site dados.gov.br'''
    def __init__(self, urlMain, dirSave):
        '''Função de inicialização da classe;
        Obs.: Sempre colocar duas barras ('//') no diretório;
        urlMain = link do site dados.gov.br que contém os arquivos do tipo json para extração
        dirSave = diretório que será armazenado as planilhas coletadas do site
        '''
        
        self.urlMain = urlMain #Url que contém todos os arquivos JSON para extração - DATASET
        self.dirSave = dirSave #Diretório para salvar arquivos
        
    def scrapingSite(self):
        ''' Responsável por raspar a página de dados do site dados.gov.br e localizar
        o endereço dos arquivos json e respectivo título;
        Função retorna o domínio e o titulo do arquivo da API'''
        
        #Solicitando resposta das informações        
        answer = requests.get(self.urlMain)
        
        #Solicitando conteudo do HTML
        answer = answer.content
    
        #Iniciando raspagem
        scrap = BeautifulSoup(answer, features = 'lxml')
        
        self.domPg2 = [] #Domínio da página que contém o url do arquivo json
        self.title_json = [] #Título JSON
        
        #Localizando todos os links da página com arquivo json e os títulos do arquivo json
        for i in scrap.find_all('a', {'class':'heading'}):
            if i.find('span').get('data-format') == 'json': #Se dado for do tipo json, armazena domínio e título
                self.domPg2.append(str(i.get('href')))
                self.title_json.append(str(i.get('title')))
        return self.domPg2, self.title_json
    
    def scrapingTable(self, dom, title):
        '''Responsável por raspar a página com os arquivos json,
        captar os arquivos json, e colocá-los em tabelas formato xlsx'''

        for link, title in zip(dom, title):
            
            #Condicional para o caso de haver '/' no título do arquivo; em caso de barras o programa não consegue salvar
            if '/' in title:
                title = title.replace('/', '-')
            
            #Solicitando resposta da pag com o link para os arquivos json
            answerPg2 = requests.get('http://dados.gov.br' + link)
            6
            #Coletando o arquivo HTML
            answerPg2 = answerPg2.content
            
            #Iniciando a raspagem
            scrapPg2 = BeautifulSoup(answerPg2, features = 'lxml')
            
            #Coletando link da API
            linkAPI = []
            for j in scrapPg2.find_all('p', {'class':'muted ellipsis'}):
                linkAPI.append(str(j.find('a').get('href')))
                
                
            #Solicitando resposta do link da API
            answerAPI = requests.get(linkAPI[0])
            
            #Armazenando os dados em DataFrame
            dataAPI = json.loads(str(answerAPI.text))
            try:
                df = pd.DataFrame(dataAPI['valores']) #PT
            except:
                try:
                    df = pd.DataFrame(dataAPI['values']) #EN
                except:
                    df = pd.DataFrame(dataAPI) #dataAPI é a própria tabela
            self.saveData(title, df)
    def saveData(self, title, df):
        '''Salvando arquivos em planilas no formato xlsx'''
        df.to_excel(self.dirSave + title + '.xlsx', index_label = None, encoding = 'utf-8', engine = 'openpyxl')
       
    def extraction(self):
        '''Extração dos dados'''
        return self.scrapingTable(self.scrapingSite()[0], self.scrapingSite()[1])

