from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import requests
import datetime
import time
import pandas as pd
import csv
import os

# Obtendo a data atual
data_atual = datetime.date.today()

def atualizar_saldo_vigencia(nome_arquivo_csv):
    
    print('Tentando carregar dados dos pregões anteriores...')
    
    df_itens = pd.read_csv(nome_arquivo_csv, sep=';')

    df_itens['Início da Vigência'] = df_itens['Início da Vigência'].astype('string')
    df_itens['Fim da Vigência'] = df_itens['Fim da Vigência'].astype('string')
    df_itens['Qtd. Saldo'] = df_itens['Qtd. Saldo'].astype('string')
    
    print('DataFrame carregado com sucesso!')
    
#atualizando o saldo
    
    for idx, row in df_itens.iterrows():

        print('Iniciando atualização do saldo, início e fim da vigência...')
        
        url = row['Link do Item']
        
        # Enviar uma solicitação GET para obter o conteúdo da página
        response = requests.get(url)
        
        # Verificar se a solicitação foi bem-sucedida
    
        if response.status_code == 200:  

            # Parsear o HTML da página com Beautiful Soup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Encontrar todas as tabelas na página
            tables = soup.find_all('table')
            
            for row in tables[1].find_all('tr'):
                # Encontra todas as colunas da linha
                cols = row.find_all('td') 


                # Verifica se há colunas suficientes na linha
                if len(cols) >= 4:

                    # Verifica se o PQ R MNT/5 está na tabela de participantes/gerenciador
                    if '160224 - PQ R MNT/5' in cols[0].text:
                        # Obtém a quantidade e saldo dos itens
                        #col1 = cols[0].text
                        #col2 = cols[1].text
                        #qtd = cols[2].text
                        saldo = cols[3].text
                        #print(f'Item encontrado. Qtd. Autorizada: {qtd}, Saldo: {saldo}')
                        inicio_vigencia = tables[0].find_all('span')[5].text.strip(), #Vig. Início ARP
                        fim_vigencia = tables[0].find_all('span')[6].text.strip(), #Vig. Fim ARP


            #Gravar saldo, inicio da vigencia e fim da vigencia
            df_itens.at[idx, 'Qtd. Saldo'] = saldo
            df_itens.at[idx, 'Início da Vigência'] = inicio_vigencia
            df_itens.at[idx, 'Fim da Vigência'] = fim_vigencia

            print(f'Saldo, início e fim da vigência do item {idx} atualizado com sucesso!')

    df_itens['Qtd. Saldo'] = df_itens['Qtd. Saldo'].str.replace('.','')
    df_itens['Qtd. Saldo'] = df_itens['Qtd. Saldo'].str.replace(',','.')

    print('Fim da atualização!')
 
    return df_itens