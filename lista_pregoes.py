from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import requests
import datetime
import time
import csv
import os



# Obtendo a data atual
data_atual = datetime.date.today()

def carregar_lista_pregoes():
    nome_arquivo = 'url_pregoes.csv'
    url_pregoes_antiga = []
    
    with open(nome_arquivo, mode='r') as file:
        reader = csv.reader(file)
        #next(reader)  # Pular o cabeçalho
        url_pregoes_antiga = [row[0] for row in reader]
    
    print('Lista de Pregões salvas no PC encontrada!')
        
    return url_pregoes_antiga

def baixar_nova_lista_pregoes(url):
    
    print('Baixando nova lista de pregões ...')
    # Configuração do WebDriver
    #options = webdriver.ChromeOptions()
    #options.add_argument('--headless')  # Executar em modo headless para não abrir uma janela do navegador
    #driver = webdriver.Chrome(options=options)
    driver = webdriver.Chrome()
    driver.get(url)

    # Selecionar a opção "Todos"
    select = Select(driver.find_element(By.NAME, 'crudTable_length'))
    select.select_by_value('-1')
    time.sleep(5)  # Esperar alguns segundos para garantir que a página carregue completamente

    # Obter e parsear o HTML da página
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    specific_url_part = 'https://contratos.sistema.gov.br/transparencia/compras/'
    url_pregoes_nova = [a_tag['href'].replace('show', 'itens') for a_tag in soup.find_all('a', href=True) if specific_url_part in a_tag['href']]
    


    # Gravar a lista em um arquivo CSV
    nome_arquivo = 'url_pregoes.csv'
    with open(nome_arquivo, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([f'Atualizado em {data_atual}'])  # Escrever a data da atualização
        writer.writerows([[url] for url in url_pregoes_nova])
        print('Nova Lista de pregões salva com sucesso!')
    
    return url_pregoes_nova