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

def baixar_nova_lista_pregoes():

    nome_arquivo = 'url_pregoes_nova.csv'
    url_pregoes_nova = []
    
    with open(nome_arquivo, mode='r') as file:
        reader = csv.reader(file)
        #next(reader)  # Pular o cabeçalho
        url_pregoes_nova = [row[0] for row in reader]
    
    print('Lendo nova lista de url dos pregões ...')

    
    return url_pregoes_nova