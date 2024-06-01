#!/usr/bin/env python
# coding: utf-8

# PARTE 1: Abrir a página do pregão que contém as informações básicas e os links para cada item

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import requests
import datetime
import time
import pandas as pd


# In[2]:


url = "https://contratos.sistema.gov.br/transparencia/compras?unidade_origem_id=9964&unidade_origem_id_text=160224+-+PARQUE+REGIONAL+DE+MANUTENCAO%2F5&lei=LEI14133&lei_text=LEI14133&persistent-table=true"


# In[3]:


#Abrindo a página desejada

driver = webdriver.Chrome()
driver.get(url)

# Encontrar o elemento select pelo ID
select_element = driver.find_element(By.NAME, 'crudTable_length')

# Criar um objeto Select
select = Select(select_element)

# Selecionar a opção "Todos"
select.select_by_value('-1')

# Esperar alguns segundos para garantir que a página carregue completamente
time.sleep(5)

# Obter o HTML da página
page_source = driver.page_source

# Fechar o WebDriver
driver.quit()

# Parsear o HTML com Beautiful Soup
soup = BeautifulSoup(page_source, 'html.parser')


# In[4]:


# Encontrar os links para cada pregão
specific_url_part = 'https://contratos.sistema.gov.br/transparencia/compras/'
links_pregoes = []

for a_tag in soup.find_all('a', href=True):
    href = a_tag['href']
    if specific_url_part in href:
        links_pregoes.append(href)
        
links_pregoes = [link.replace('show', 'itens') for link in links_pregoes]


# In[9]:
# Obtendo a data atual
data_atual = datetime.date.today()

#Gravando em arquivo CSV
pd.DataFrame(links_pregoes).to_csv('lista_pregoes_'+str(data_atual)+'.csv',index=False)

#-----------------------------------------------------------------------------------------------------------------





# SEGUNDA PARTE: entrar no link de cada pregão para obter o link de cada item

# In[28]:


lista_pregoes = pd.read_csv('lista_pregoes_'+str(data_atual)+'.csv')
lista_pregoes.columns = ['Link de cada Pregão']


# In[30]:


link_itens = []

for i in range(len(lista_pregoes)):
    
    url = lista_pregoes['Link de cada Pregão'][i]
    
    #Abrindo a página desejada

    driver = webdriver.Chrome()
    driver.get(url)

    # Encontrar o elemento select pelo ID
    select_element = driver.find_element(By.NAME, 'crudTable_length')

    # Criar um objeto Select
    select = Select(select_element)

    # Selecionar a opção "Todos"
    select.select_by_value('-1')

    # Esperar alguns segundos para garantir que a página carregue completamente
    time.sleep(5)

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
            link_itens.append(href)    

link_itens = [url for url in link_itens if 'show' in url]


# In[31]:

# Obtendo a data atual
data_atual = datetime.date.today()

#Gravar a lista de pregões

pd.DataFrame(link_itens).to_csv('lista_links_itens'+str(data_atual)+'.csv', index=False)


#-----------------------------------------------------------------------------------------------------------------------------------------------

# TERCEIRA PARTE: Entrar no link de cada item para obter as informações

# In[4]:

#Carregando a lista de url dos itens

lista_links_itens = pd.read_csv('lista_links_itens'+str(data_atual)+'.csv')
lista_links_itens.columns = ['Link de cada Item']


# In[5]:


#Para obter as informações de cada item

linhas = []

for i in range(len(lista_links_itens)):
        
    # URL da página que contém as tabelas
    url = lista_links_itens['Link de cada Item'][i]
    # Enviar uma solicitação GET para obter o conteúdo da página
    response = requests.get(url)
    # Verificar se a solicitação foi bem-sucedida
    
    if response.status_code == 200:              
        
        # Parsear o HTML da página com Beautiful Soup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        #Pregão
        pregao = soup.find_all('div', class_='header-title')[1].text.strip().replace('Itens da compra: 160224 - ','')
        
        # Encontrar todas as tabelas na página
        tables = soup.find_all('table')
        #Define a nova linha
        linha = [
            pregao, #Pregão
            tables[0].find_all('span')[0].text.strip(), #Item
            tables[0].find_all('span')[2].text.strip(), #Descrição
            tables[0].find_all('span')[3].text.strip(), #Descrição detalhada
            #tables[0].find_all('span')[4].text.strip(), #Qtd. Total
            tables[0].find_all('span')[5].text.strip(), #Vig. Início ARP
            tables[0].find_all('span')[6].text.strip(), #Vig. Fim ARP
            tables[1].find_all('td')[0].text.strip(), #Unidade
            #tables[1].find_all('td')[1].text.strip(), #Tipo UASG
            tables[1].find_all('td')[2].text.strip(), #Qtd. Autorizada
            
            tables[2].find_all('td')[0].text.strip(), #Fornecedor
            #tables[2].find_all('td')[1].text.strip(), #Qtd. Homologada
            tables[2].find_all('td')[2].text.strip(), #Val. Unitário
            #tables[2].find_all('td')[3].text.strip(), #Val. Negociado      
            tables[1].find_all('td')[3].text.strip(), #Qtd. Saldo
            lista_links_itens['Link de cada Item'][i], #link de cada item no Comprasgov
            ]
        #Append a linha
        linhas.append(linha)


# In[6]:


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
    


# In[8]:


headers[1] = "Número do Item"
headers[2] = "Descrição"
headers[3] = "Descrição Detalhada"
headers[4] = "Início da Vigência"
headers[5] = "Fim da Vigência"


# In[18]:


df_itens = pd.DataFrame(linhas, columns = headers)


# In[19]:


#Corrigindo os valores que são numéricos

df_itens['Qtd. Autorizada'] = df_itens['Qtd. Autorizada'].str.replace('.','')
df_itens['Qtd. Autorizada'] = df_itens['Qtd. Autorizada'].str.replace(',','.')

df_itens['Val. Unitário'] = df_itens['Val. Unitário'].str.replace('.','')
df_itens['Val. Unitário'] = df_itens['Val. Unitário'].str.replace(',','.')

df_itens['Qtd. Saldo'] = df_itens['Qtd. Saldo'].str.replace('.','')
df_itens['Qtd. Saldo'] = df_itens['Qtd. Saldo'].str.replace(',','.')


# In[21]:


tipo_compra = []
numero_compra_pregao = []
ano_compra_pregao = []


for i in range(len(df_itens['Número da Compra'])):
    tipo = df_itens['Número da Compra'][i].split(' ')[0]
    numero_pregao = df_itens['Número da Compra'][i].split(' ')[2].split('/')[0]
    ano_pregao = df_itens['Número da Compra'][i].split(' ')[2].split('/')[1]
    
    tipo_compra.append(tipo)
    numero_compra_pregao.append(numero_pregao)
    ano_compra_pregao.append(ano_pregao)


# In[22]:


df_itens['Tipo de Compra'] = tipo_compra
df_itens['Número do Pregão'] = numero_compra_pregao
df_itens['Ano do Pregão'] = ano_compra_pregao


# In[25]:


nome_arquivo_csv = "df_itens_atualizado_em_" +str(data_atual) + '.csv'


# In[28]:


# Exportando o DataFrame para um arquivo CSV com delimitador ';' e codificação UTF-8
df_itens.to_csv(nome_arquivo_csv+'.csv', sep=';', encoding='utf-8', index=False)


#------------------------------------------------------------------------------------------------------------------------------------

#PARTE QUATRO - I - obtendo as colunas unidade de fornecimento, objeto dos pregões

# In[4]:


df_itens['UASG'] = df_itens['Unidade'].str[:6]


# In[6]:


print("Há " + str(len(df_itens['Número da Compra'].unique())) + " licitações cadastradas.")


# In[7]:


lista_pregao_site_antigo = []

for i in range(len(df_itens)):
  url = "http://comprasnet.gov.br/ConsultaLicitacoes/download/download_editais_detalhe.asp?coduasg=" + str(df_itens['UASG'][i])+"&modprp=5&numprp=" + str(df_itens['Número do Pregão'][i]) + str(df_itens['Ano do Pregão'][i])
  lista_pregao_site_antigo.append(url)

print(lista_pregao_site_antigo[:2])


# In[8]:


lista_pregao_site_antigo = list(set(lista_pregao_site_antigo))

print('Há ' + str(len(lista_pregao_site_antigo)) + ' url na lista de pregões.')


# #PARTE QUATRO - II - obter as informações de cada url (unidade, objeto do pregão)

# In[9]:


linhas_pregao_site_antigo = []

for url in lista_pregao_site_antigo:

  response = requests.get(url)

  soup = BeautifulSoup(response.content, 'html.parser')

  for i in range(len(soup.find_all('table')[1].find_all('span', class_ = 'tex3b')[2:-1])):

    numeropregao_ano = soup.find_all('table')[1].find_all('span', class_ = 'tex3b')[0].get_text(separator = ' ').split('Nº')[1].strip()

    objeto = soup.find_all('table')[4].find_all('tr')[7].find_all('td')[2].find_all('p')[0].find('b', string='Objeto:').next_sibling.strip()

    numero_item = soup.find_all('table')[1].find_all('span', class_ = 'tex3b')[2:-1][i].get_text(separator = ' ').split('-')[0].strip()
    descricao_item = soup.find_all('table')[1].find_all('span', class_ = 'tex3b')[2:-1][i].get_text(separator = ' ').split('-')[1].strip()

    descricao_complementar = soup.find_all('table')[1].find_all('span', class_ = 'tex3')[i].text
    fim = soup.find_all('table')[1].find_all('span', class_ = 'tex3')[i].get_text(separator = ' ').find('Tratamento Diferenciado')
    descricao_complementar = descricao_complementar[:fim-1]

    unidade_medida = soup.find_all('table')[1].find_all('span',class_='tex3')[i]
    inicio = unidade_medida.get_text(separator = ' ').find('Unidade de fornecimento:')
    unidade_medida = unidade_medida.get_text(separator = ' ')[inicio:].split(':')[1].strip()

    linha = [numeropregao_ano,
              objeto,
              numero_item,
              descricao_item,
              descricao_complementar,
              unidade_medida
            ]


    linhas_pregao_site_antigo.append(linha)


# In[10]:


headers = ["Número da Compra","Objeto","Número do Item","Descrição", "Descrição Complementar","Unidade de Fornecimento"]


# In[12]:


df_itens_site_antigo = pd.DataFrame(linhas_pregao_site_antigo, columns = headers)

# In[13]:


df_itens['Número da Compra'] = df_itens['Número da Compra'].astype('string')
df_itens['Número do Item'] = df_itens['Número do Item'].astype('string')

df_itens_site_antigo['Número da Compra'] = df_itens_site_antigo['Número da Compra'].astype('string')
df_itens_site_antigo['Número do Item'] = df_itens_site_antigo['Número do Item'].astype('string')


# In[19]:


ano_pregao = []
numero_pregao = []

for i in range(len(df_itens_site_antigo['Número da Compra'])):
    
    numero = df_itens_site_antigo['Número da Compra'][i].split('/')[0]
    numero_pregao.append(numero)
    
    ano = df_itens_site_antigo['Número da Compra'][i].split('/')[1]
    ano_pregao.append(ano)

df_itens_site_antigo['Ano do Pregão'] = ano_pregao
df_itens_site_antigo['Número do Pregão'] = numero_pregao

df_itens_site_antigo['Ano do Pregão'] = df_itens_site_antigo['Ano do Pregão'].astype('string')
df_itens_site_antigo['Número do Pregão'] = df_itens_site_antigo['Número do Pregão'].astype('string')




# In[22]:


df_itens['Ano do Pregão'] = df_itens['Ano do Pregão'].astype('string')
df_itens['Número do Pregão'] = df_itens['Número do Pregão'].astype('string')
df_itens['Número do Item'] = df_itens['Número do Item'].astype('int')
df_itens['Número do Item'] = df_itens['Número do Item'].astype('string')


# In[28]:


#Criando novas colunas que servirão como key para o merge
df_itens['key'] = df_itens['Número do Pregão'] + '_' + df_itens['Ano do Pregão'] + '_' + df_itens['Número do Item']
df_itens_site_antigo['key'] = df_itens_site_antigo['Número do Pregão'] + '_' + df_itens_site_antigo['Ano do Pregão']+ '_' + df_itens_site_antigo['Número do Item']


# In[29]:


df_merged = df_itens.merge(df_itens_site_antigo, how = 'outer', on = ['key'])
df_merged.shape


# In[30]:


df_merged.columns


# In[32]:


df_final = df_merged.drop(columns=['key','Número da Compra_y','Número do Item_y', 'Descrição_y', 'Descrição Complementar', 'Ano do Pregão_y', 'Número do Pregão_y'])

# In[33]:


df_final.columns = ['Número da Compra', 'Número do Item', 'Descrição',
       'Descrição Detalhada', 'Início da Vigência', 'Fim da Vigência',
       'Unidade', 'Qtd. Autorizada', 'Fornecedor', 'Val. Unitário',
       'Qtd. Saldo', 'Link do Item', 'Tipo de Compra', 'Número do Pregão', 'Ano do Pregão',
       'UASG', 'Objeto', 'Unidade de Fornecimento']


# ETAPA FINAL

# In[37]:


nome_arquivo_csv = "ArquivoFinal"+str(data_atual) + '.csv'


# In[38]:


# Exportando o DataFrame para um arquivo CSV com delimitador ';' e codificação UTF-8
df_final.to_csv(nome_arquivo_csv + '.csv', sep=';', encoding='utf-8', index=False)

