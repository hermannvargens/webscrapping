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

def merge_df(df_itens_novos,df_itens_novos_site_antigo, tipo_compra):
    
    #Criando novas colunas que servirão como key para o merge
    df_itens_novos['key'] = df_itens_novos['Número do Pregão'] + '_' + df_itens_novos['Ano do Pregão'] + '_' + df_itens_novos['Número do Item']
    df_itens_novos_site_antigo['key'] = df_itens_novos_site_antigo['Número do Pregão'] + '_' + df_itens_novos_site_antigo['Ano do Pregão']+ '_' + df_itens_novos_site_antigo['Número do Item']

    #Apagando as colunas desnecessárias
    
    df_itens_novos_site_antigo = df_itens_novos_site_antigo[['Objeto','Unidade de Fornecimento','key']]

    
    #obtendo o df final
    
    df_itens_novos = df_itens_novos.merge(df_itens_novos_site_antigo, how = 'left', on = ['key'])

    
    df_itens_novos['Descrição'] = df_itens_novos['Descrição'].str.replace(';',',')
    df_itens_novos['Descrição Detalhada'] = df_itens_novos['Descrição Detalhada'].str.replace(';',',')
    df_itens_novos['Objeto'] = df_itens_novos['Objeto'].str.replace(';',',')
    df_itens_novos['Unidade de Fornecimento'] = df_itens_novos['Unidade de Fornecimento'].str.replace(';',',')
    df_itens_novos.drop(columns=['key'], inplace=True)

    return df_itens_novos