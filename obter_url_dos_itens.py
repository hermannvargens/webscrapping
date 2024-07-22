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

def obter_url_dos_itens(novos_pregoes):
    
    url_itens = []

    for url in novos_pregoes:
        
        try:

            # Configuração do WebDriver
            #options = webdriver.ChromeOptions()
            #options.add_argument('--headless')  # Executar em modo headless para não abrir uma janela do navegador
            #driver = webdriver.Chrome(options=options)
            driver = webdriver.Chrome()
            driver.get(url)
    
            #apagar
            print(f'Obtendo dados da url {url}')
    
            # Encontrar o elemento select pelo ID
            select_element = driver.find_element(By.NAME, 'crudTable_length')
    
            # Criar um objeto Select
            select = Select(select_element)
    
            # Selecionar a opção "Todos"
            select.select_by_value('-1')
    
            # Esperar alguns segundos para garantir que a página carregue completamente
            time.sleep(60)
    
            # Obter o HTML da página
            page_source = driver.page_source
    
            # Fechar o WebDriver
            driver.quit()
    
            # Parsear o HTML com Beautiful Soup
            soup = BeautifulSoup(page_source, 'html.parser')
    
            # Encontrar os links para cada item
            specific_url_part = 'https://contratos.sistema.gov.br/transparencia/compras/'
    
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                if specific_url_part in href:
                    url_itens.append(href)    
    
            url_itens = [url for url in url_itens if 'show' in url]
    
        #apagar
        #print(url_itens)
    
        except Exception as e:
            print(f"Erro ao processar a URL {url}: {e}")
        
    
        # Gravar a lista em um arquivo CSV
        nome_arquivo = 'url_itens_novos.csv'
        with open(nome_arquivo, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([f'Atualizado em {data_atual}'])  # Escrever a data da atualização
            writer.writerows([[url] for url in url_itens])
            print('Nova Lista de url dos itens salva com sucesso!')
    
        
    return url_itens