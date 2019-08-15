#Importando modulos
import requests
import json
import pandas as pd
from bs4 import BeautifulSoup


#Criando a classe de aquisicao de dados do IBGE
class getIBGE:

    def __init__(self):
        #Parametros
        self.urlDescribe = 'http://api.sidra.ibge.gov.br/desctabapi.aspx?c='
        self.urlService = 'http://api.sidra.ibge.gov.br/values'
      
    def scrapingdata(self,table,periodo = 'last',variavel = 'all'):
    #def describeSite(self,table):
        
        #Requisicao da informacao
        html = requests.get(self.urlDescribe+str(table))
    
        #Html do conteudo
        conteudo = html.content
        
        #Iniciando o processo de raspagem
        scrap = BeautifulSoup(conteudo,'html.parser')
        
        #Colentando a clssificacao da tabela
        classif = scrap.find(id='lstClassificacoes_lblIdClassificacao_0')
        
        classificacao = "C"+classif.text
    
        #parametros
        tabela = '/t/'+str(table)
        periodo = '/p/'+str(periodo)
        variavel = '/v/'+str(variavel)
        nivelterritorial = '/n3/52/n6/in n3 52'
        classifi = '/'+classificacao+'/all'
        
        #Parametros
        params = tabela + periodo + variavel + nivelterritorial+classifi+'/h/y'
    
           
        #Requisicao da informacao
        getdata = requests.get(self.urlService+params)
        data = json.loads(str(getdata.text))

        #Criando um dataframe
        df = pd.DataFrame(data=data)
        df.columns = df.iloc[0].values
        df = df.drop(df.index[0])
    
        #Retornando o valor
        return df
    
    def saveData(self,dataframe,arquivoSaida):
        
        #Salvando o arquivo em excel
        dataframe.to_excel(arquivoSaida,index_label=None,encoding='utf-8')
