import csv
import escola
import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def get_column_of_csv(filename, column):
    with open("./challenge_01/base_dados_teste.csv", "r", encoding='utf8') as stream:
        reader = csv.DictReader(stream)
        for row in reader:
            yield row[column]

servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico)
colegio = escola.Escola
lista_escolas = []
escolas = ["Escola Test"]

for name in get_column_of_csv('./challenge_01/base_dados_teste.csv', "Nome da Escola"):
    escolas.append(name)
    
for escola in escolas:
    print(escola)
    
for escola in escolas:
    try:
        navegador.get("https://www.google.com")
        navegador.find_element(By.XPATH, '//*[@id="APjFqb"]').clear()
        navegador.find_element(By.XPATH, '//*[@id="APjFqb"]').send_keys(escola.format(str) + Keys.RETURN)
        nome_escola = navegador.find_element(By.CSS_SELECTOR, ".qrShPb").text
        endereco_escola = navegador.find_element(By.CSS_SELECTOR, ".LrzXr").text
        lista_escolas.append(colegio(nome_escola=nome_escola, endereco_escola=endereco_escola))
        
    except:
        print('Erro!')

with open('challenge_01/base_nova.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csv.writer(csvfile).writerow(["Nome da Escola", "Endereço"])
    for escola in lista_escolas:
        csv.writer(csvfile).writerow([escola.nome_escola, escola.endereco_escola])
        
            