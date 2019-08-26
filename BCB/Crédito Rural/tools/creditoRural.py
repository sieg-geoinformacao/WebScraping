# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 08:28:14 2019

@author: savio.pereira
"""

''' Por indisponibili'''

from bs4 import BeautifulSoup
import requests
import json
import pandas as pd

class getCreditoRural:
    '''
    Classe responsável por coletar dados sobre crédito rural no site do BCB
    '''
    def __init__(self, dir, 
                 link = 'https://dadosabertos.bcb.gov.br/dataset/matrizdadoscreditorural'):
        '''
        Função de inicialização;
        Recebe dois parâmetros:
            dir = diretório para salvar planilhas
            link = link do site para coleta
        '''
        
        self.dir = dir
        self.link = link
        
    def initialScraping(self):
        '''
        Inicia a raspagem dos dados na página principal do BCB sobre crédito rural
        '''
        #Solicitando resposta
        answer = requests.get(self.link)
        answer = answer.content
        
        #Iniciando a raspagem dos dadosd
        htmlSoup = BeautifulSoup(answer, features='lxml')
        
        #Lista que receberá o dominio para coleta de cada tabela
        domList = []
        
        #Lista que receberá o titulo de cada tabela
        titleList = []
        
        for i in htmlSoup.find_all('a', {'class':'heading'}):
            if i.find('span').get('data-format') == 'json':
                domList.append(i.get('href'))
                titleList.append(i.get('title'))
        return domList, titleList
    
    def variablesScraping(self):
        '''
        Realiza a raspagem das variáveis no site do BCB
        '''
        #Chamando a função initialScraping
        dom, title = self.initialScraping()
         
        linkDoc = 'https://olinda.bcb.gov.br/olinda/servico/SICOR/versao/v2/documentacao'
         
        #Solicitando resposta
        answer = requests.get(linkDoc)
        answer = answer.content
         
        #Iniciando a raspagem
        htmlSoup = BeautifulSoup(answer, features='lxml')
         
        #Lista que irá receber o código da variável
        codeVar = []
        #Lista que irá receber nome da variável
        nameVar = []
         
        #Coletando o código e o nome das variáveis de cada tabela
        for i in htmlSoup.find_all('script')[3].text.split('\n'):
            if 'nome' in i:
                if ('TipoResultado' in i) or ('SICOR' in i) or ('v2' in i):
                    pass
                else:
                    codeVar.append(i)
            if 'titulo' in i:
                if ('Tipo de Resultado' in i) or ('Matriz de Dados') in i:
                    pass
                else:
                    nameVar.append(i)
                    
        #Tratamento das strings das lista codeVar e nameVar
        
        for i in range(len(codeVar)):
            codeVar[i] = codeVar[i].strip()
            codeVar[i] = codeVar[i].replace('"nome" : ', '').replace(',','')
            codeVar[i] = codeVar[i].replace('"', '')
            
        for i in range(len(nameVar)):
            nameVar[i] = nameVar[i].strip()
            nameVar[i] = nameVar[i].replace('"titulo" : ', '').replace(',','')
            
            
        #Localizando os index na lista nameVar que correspondem aos titulos das tabelas
        index = []
        for j in title:
            count = 0
            for k in nameVar:
                if k == ('"' + j.replace(',','') + '"'):
                    index.append(count)
                count += 1
        index.append(len(nameVar))
         
        return index, codeVar, nameVar
         
    def organizationVariables(self):
        '''
        Organiza as variáveis
        '''
        #Chamando as funções initialScraping e variablesScraping
        dom, title = self.initialScraping()
        index, codeVar, nameVar = self.variablesScraping()
        
        
        #Armazendando as variáveis em dicionários
        conMun = {}
        for i in range(1, index[1]):
            conMun[nameVar[i]] = codeVar[i]
        
        conCustMun = {}
        for i in range(index[1]+1, index[2]):
            conCustMun[nameVar[i]] = codeVar[i]
        
        conComer = {}
        for i in range(index[2]+1, index[3]):
            conComer[nameVar[i]] = codeVar[i]
        
        conCust = {}
        for i in range(index[3]+1, index[4]):
            conCust[nameVar[i]] = codeVar[i]
        
        conFx = {}
        for i in range(index[4]+1, index[5]):
            conFx[nameVar[i]] = codeVar[i]
        
        conFtrec = {}
        for i in range(index[5]+1, index[6]):
            conFtrec[nameVar[i]] = codeVar[i]
        
        conFtif = {}
        for i in range(index[6]+1, index[7]):
            conFtif[nameVar[i]] = codeVar[i]
        
        conFxuf = {}
        for i in range(index[7]+1, index[8]):
            conFxuf[nameVar[i]] = codeVar[i]
        
        conInvsMun = {}
        for i in range(index[8]+1, index[9]):
            conInvsMun[nameVar[i]] = codeVar[i]
        
        conInvsUf = {}
        for i in range(index[9]+1, index[10]):
            conInvsUf[nameVar[i]] = codeVar[i]
        
        conPrg = {}
        for i in range(index[10]+1, index[11]):
            conPrg[nameVar[i]] = codeVar[i]
        
        conPrgUf = {}
        for i in range(index[11]+1, index[12]):
            conPrgUf[nameVar[i]] = codeVar[i]
        
        conReg = {}
        for i in range(index[12]+1, index[13]):
            conReg[nameVar[i]] = codeVar[i]
        
        conRegGen = {}
        for i in range(index[13]+1, index[14]):
            conRegGen[nameVar[i]] = codeVar[i]
        
        conSeg = {}
        for i in range(index[14]+1, index[15]):
            conSeg[nameVar[i]] = codeVar[i]
        
        conRegSeg = {}
        for i in range(index[15]+1, index[16]):
            conRegSeg[nameVar[i]] = codeVar[i]
        
        conTpPes = {}
        for i in range(index[16]+1, index[17]):
            conTpPes[nameVar[i]] = codeVar[i]
        
        key = [conMun,
                 conCustMun,
                 conComer,
                 conCust,
                 conFx,
                 conFtrec,
                 conFtif,
                 conFxuf,
                 conInvsMun,
                 conInvsUf,
                 conPrg,
                 conPrgUf,
                 conReg,
                 conRegGen,
                 conSeg,
                 conRegSeg,
                 conTpPes]
        
        dicVar = {}
        for i in range(len(key)):
            dicVar[title[i]] = key[i]
            
        nameSite = []
        for i in range(len(index)):
            try:
                nameSite.append(codeVar[index[i]])
            except:
                pass
        
        return dicVar, nameSite  
    
    def scrapingTable(self):
        '''
        Realiza a raspagem das tabelas
        '''
        #Chamando as funções initialScraping, variablesScraping e organizationVariables
        dom, title = self.initialScraping()
        index, codeVar, nameVar = self.variablesScraping()
        dicVar, nameSite = self.organizationVariables()
        
        
        #Adicionando as variáveis a URL
        count = 0
        for i,j in zip(title, dom):
            #URL da API
            urlAPI = 'https://olinda.bcb.gov.br/olinda/servico/SICOR/versao/v2/odata/' + nameSite[count] + '?$top=100&$format=json'
            count += 1
            for k in range(len(list(dicVar[i].keys()))):
                if k == 0:
                    urlAPI = urlAPI + '&$select=' + dicVar[i][list(dicVar[i].keys())[k]]
                else:
                    urlAPI = urlAPI + ',' + dicVar[i][list(dicVar[i].keys())[k]]
            try:
                #Solicitando resposta
                answer = requests.get(urlAPI)
            
                #Coletando os dados
                data = json.loads(str(answer.text))
            
                #Criando o DataFrame
                df = pd.DataFrame(data['value'])
                
                df.to_excel(self.dir + str(i) + '.xlsx',
                            index_label=None, encoding='utf-8', engine = 'openpyxl')
            except:
                print(f'Planila {str(i)} não deu certo. Verificar o link: {urlAPI}')