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

def obter_dados_site_novo(url_itens_novos):

    print(f'Obtendo os dados de cada item...')

    linhas = []

    for url in url_itens_novos:
        
        # Enviar uma solicitação GET para obter o conteúdo da página
        response = requests.get(url)
     
        # Verificar se a solicitação foi bem-sucedida

        if response.status_code == 200:              

            # Parsear o HTML da página com Beautiful Soup
            soup = BeautifulSoup(response.content, 'html.parser')

            #Pregão
            pregao = soup.find_all('div', class_='header-title')[1].text.strip().replace('Itens da compra: ','')

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
                        uasg_gerenciadora = cols[0].text
                        col2 = cols[1].text
                        qtd = cols[2].text
                        saldo = cols[3].text
                        #print(f'Item encontrado. Qtd. Autorizada: {qtd}, Saldo: {saldo}')

                       #Define a nova linha
                        linha = [
                            pregao, #Pregão
                            tables[0].find_all('span')[0].text.strip(), #Item
                            tables[0].find_all('span')[2].text.strip(), #Descrição
                            tables[0].find_all('span')[3].text.strip(), #Descrição detalhada
                            #tables[0].find_all('span')[4].text.strip(), #Qtd. Total
                            tables[0].find_all('span')[5].text.strip(), #Vig. Início ARP
                            tables[0].find_all('span')[6].text.strip(), #Vig. Fim ARP
                            uasg_gerenciadora, #Unidade
                            #tables[1].find_all('td')[1].text.strip(), #Tipo UASG
                            qtd, #Qtd. Autorizada
                            tables[2].find_all('td')[0].text.strip(), #Fornecedor
                            #tables[2].find_all('td')[1].text.strip(), #Qtd. Homologada
                            tables[2].find_all('td')[2].text.strip(), #Val. Unitário
                            #tables[2].find_all('td')[3].text.strip(), #Val. Negociado      
                            saldo, #Qtd. Saldo
                            url, #link de cada item no Comprasgov
                            ]
                        
                        #Append a linha
                        linhas.append(linha)
                                    
            
    #Para obter os cabeçalhos

    headers = [
        "Número da Compra",
        tables[0].find_all('strong')[0].text.strip(), #Item
        tables[0].find_all('strong')[2].text.strip(), #Descrição
        tables[0].find_all('strong')[3].text.strip(), #Descrição detalhada
        #tables[0].find_all('strong')[4].text.strip(), #Qtd. Total
        tables[0].find_all('strong')[5].text.strip(), #Vig. Início ARP
        tables[0].find_all('strong')[6].text.strip(), #Vig. Fim ARP
        tables[1].find_all('th')[0].text.strip(), #Unidade
        #tables[1].find_all('th')[1].text.strip(), #Tipo UASG
        tables[1].find_all('th')[2].text.strip(), #Qtd. Autorizada

        tables[2].find_all('th')[0].text.strip(), #Fornecedor
        #tables[2].find_all('th')[1].text.strip(), #Qtd. Homologada
        tables[2].find_all('th')[2].text.strip(), #Val. Unitário
        #tables[2].find_all('th')[3].text.strip(), #Val. Negociado
        tables[1].find_all('th')[3].text.strip(), #Qtd. Saldo
        'Link do Item'
    ]

    headers[1] = "Número do Item"
    headers[2] = "Descrição"
    headers[3] = "Descrição Detalhada"
    headers[4] = "Início da Vigência"
    headers[5] = "Fim da Vigência"

    #transformando os dados em um dataframe

    df_itens_novos = pd.DataFrame(linhas, columns = headers)

    #Corrigindo os valores que são numéricos

    df_itens_novos['Qtd. Autorizada'] = df_itens_novos['Qtd. Autorizada'].str.replace('.','')
    df_itens_novos['Qtd. Autorizada'] = df_itens_novos['Qtd. Autorizada'].str.replace(',','.')

    df_itens_novos['Val. Unitário'] = df_itens_novos['Val. Unitário'].str.replace('.','')
    df_itens_novos['Val. Unitário'] = df_itens_novos['Val. Unitário'].str.replace(',','.')

    df_itens_novos['Qtd. Saldo'] = df_itens_novos['Qtd. Saldo'].str.replace('.','')
    df_itens_novos['Qtd. Saldo'] = df_itens_novos['Qtd. Saldo'].str.replace(',','.')

    
    #Inserindo novas colunas
    
    uasg_gerenciadora = []
    tipo_compra = []
    numero_compra_pregao = []
    ano_compra_pregao = []


    for i in range(len(df_itens_novos['Número da Compra'])):
        
        uasg = df_itens_novos['Número da Compra'][i].split(' ')[0]
        tipo = df_itens_novos['Número da Compra'][i].split(' ')[2]
        numero_pregao = df_itens_novos['Número da Compra'][i].split(' ')[4].split('/')[0]
        ano_pregao = df_itens_novos['Número da Compra'][i].split(' ')[4].split('/')[1]
                
        uasg_gerenciadora.append(uasg)
        tipo_compra.append(tipo)
        numero_compra_pregao.append(numero_pregao)
        ano_compra_pregao.append(ano_pregao)
        
    df_itens_novos['UASG'] = uasg_gerenciadora
    df_itens_novos['Tipo de Compra'] = tipo_compra
    df_itens_novos['Número do Pregão'] = numero_compra_pregao
    df_itens_novos['Ano do Pregão'] = ano_compra_pregao


    #corrigindo o tipo
    df_itens_novos['Número do Item'] = df_itens_novos['Número do Item'].astype(int)
    df_itens_novos['Número do Item'] = df_itens_novos['Número do Item'].astype('string')
    
    df_itens_novos['Número do Pregão'] = df_itens_novos['Número do Pregão'].astype(int)
    df_itens_novos['Número do Pregão'] = df_itens_novos['Número do Pregão'].astype('string')
    
    df_itens_novos['Ano do Pregão'] = df_itens_novos['Ano do Pregão'].astype(int)
    df_itens_novos['Ano do Pregão'] = df_itens_novos['Ano do Pregão'].astype('string')

    print(f'O Parque/5 possui {len(df_itens_novos)} itens neste pregão.')


    return df_itens_novos
    
    
#################################################################################################

def obter_unidade_objeto(df_itens_novos):

    print('Iniciando a obtenção da Unidade de Fornecimento de cada item e o Objeto do Pregão...')
    
    #Obtendo as novas URL dos pregões

    lista_pregao_site_antigo = []
    
    for i in range(len(df_itens_novos)):
      url = "http://comprasnet.gov.br/ConsultaLicitacoes/download/download_editais_detalhe.asp?coduasg=" + str(df_itens_novos['UASG'][i])+"&modprp=5&numprp=" + str(df_itens_novos['Número do Pregão'][i]) + str(df_itens_novos['Ano do Pregão'][i])
      lista_pregao_site_antigo.append(url)
    
    lista_pregao_site_antigo = list(dict.fromkeys(lista_pregao_site_antigo))

    #obter os dados do pregão na primeira página

    linhas = []
    
    for url in lista_pregao_site_antigo:

        print(f'Obtendo os dados da url {url}')
    
        #Abrindo a página desejada
    
        driver = webdriver.Chrome()
        driver.get(url)
        #options = webdriver.ChromeOptions()
        #options.add_argument('--headless')  # Executar em modo headless para não abrir uma janela do navegador
        time.sleep(60)  # Aguarde a página carregar
    
        for i in range(len(driver.find_elements(By.XPATH, "//span[@class='tex3b']")[2:-1])):
            
            numeropregao_ano = driver.find_elements(By.XPATH, "//span[@class='tex3b']")[0].text.split('Nº')[1].strip()
            objeto = driver.find_element(By.XPATH, "//p[contains(text(),'Objeto:')]").text.split('\n')[1]
            numero_item = driver.find_elements(By.XPATH, "//span[@class='tex3b']")[i+2].text.split('-')[0].strip()
            descricao_item = driver.find_elements(By.XPATH, "//span[@class='tex3b']")[i+2].text.split('-')[1].strip()
            descricao_complementar = driver.find_elements(By.XPATH, "//span[@class='tex3']")[i].text.split('\n')[0]
            unidade_medida = driver.find_elements(By.XPATH, "//span[@class='tex3']")[i].text.split('\n')[5].split(':')[1].strip()
        
            dados = [numeropregao_ano, objeto, numero_item, descricao_item, descricao_complementar, unidade_medida]
            
            linhas.append(dados)
    
        
        #verificar se tem próxima página para obter os dados
        
        while True:
            try:
                # Tente encontrar o botão "Próxima" e clique nele
                next_button = driver.find_element(By.ID, "proximas").click()
                
                time.sleep(10)  # Aguarde a página carregar
                
                for i in range(len(driver.find_elements(By.XPATH, "//span[@class='tex3b']")[2:-1])):
                    
                    numeropregao_ano = driver.find_elements(By.XPATH, "//span[@class='tex3b']")[0].text.split('Nº')[1].strip()
                    objeto = driver.find_element(By.XPATH, "//p[contains(text(),'Objeto:')]").text.split('\n')[1]
                    numero_item = driver.find_elements(By.XPATH, "//span[@class='tex3b']")[i+2].text.split('-')[0].strip()
                    descricao_item = driver.find_elements(By.XPATH, "//span[@class='tex3b']")[i+2].text.split('-')[1].strip()
                    descricao_complementar = driver.find_elements(By.XPATH, "//span[@class='tex3']")[i].text.split('\n')[0]
                    unidade_medida = driver.find_elements(By.XPATH, "//span[@class='tex3']")[i].text.split('\n')[5].split(':')[1].strip()
                
                    dados = [numeropregao_ano, objeto, numero_item, descricao_item, descricao_complementar, unidade_medida]
                    
                    linhas.append(dados)
                    
            except:
                # Fechar o WebDriver
                driver.quit()
                # Se não encontrar o botão "Próxima", saia do loop
                break



    #Cabeçalho
    headers = ["Número da Compra","Objeto","Número do Item","Descrição", "Descrição Complementar","Unidade de Fornecimento"]
    
    
    #transformando os dados em dataframe
    df_itens_novos_site_antigo = pd.DataFrame(linhas, columns = headers)

    #apagar
    #print('imprimir df_itens_novos_site_antigo')
    
    
    #obtendo o número do pregão e o ano
    
    ano_pregao = []
    numero_pregao = []
    
    for i in range(len(df_itens_novos_site_antigo['Número da Compra'])):
        
        numero = df_itens_novos_site_antigo['Número da Compra'][i].split('/')[0]
        numero_pregao.append(numero)
        
        ano = df_itens_novos_site_antigo['Número da Compra'][i].split('/')[1]
        ano_pregao.append(ano)
    
    df_itens_novos_site_antigo['Ano do Pregão'] = ano_pregao
    df_itens_novos_site_antigo['Número do Pregão'] = numero_pregao
    
    df_itens_novos_site_antigo['Ano do Pregão'] = df_itens_novos_site_antigo['Ano do Pregão'].astype(int)
    df_itens_novos_site_antigo['Ano do Pregão'] = df_itens_novos_site_antigo['Ano do Pregão'].astype('string')
    
    df_itens_novos_site_antigo['Número do Pregão'] = df_itens_novos_site_antigo['Número do Pregão'].astype(int)
    df_itens_novos_site_antigo['Número do Pregão'] = df_itens_novos_site_antigo['Número do Pregão'].astype('string')

    df_itens_novos_site_antigo['Número do Item'] = df_itens_novos_site_antigo['Número do Item'].astype(int)
    df_itens_novos_site_antigo['Número do Item'] = df_itens_novos_site_antigo['Número do Item'].astype('string')

    df_itens_novos_site_antigo['Objeto'] = df_itens_novos_site_antigo['Objeto'].str.replace('Objeto: Objeto: Pregão Eletrônico - ','')

    print(f'Dados de Objeto e Unidade de Fornecimento obtidos sucesso. Este Pregão possuía inicialmente {len(df_itens_novos_site_antigo)} itens.')

    return df_itens_novos_site_antigo