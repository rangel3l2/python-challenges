import csv
import escola

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico)
colegio = escola.Escola

escolas = ["Escola Municipal Prof. Ramez Tebet", "Escola Estadual Fernando Corrêa", "elite tres lagoas"]
lista_escolas = []

for escola in escolas:
    try:
        navegador.get("https://www.google.com")
        navegador.find_element(By.XPATH, '//*[@id="APjFqb"]').clear()
        navegador.find_element(By.XPATH, '//*[@id="APjFqb"]').send_keys(escola + Keys.RETURN)
        nome_escola = navegador.find_element(By.CSS_SELECTOR, ".qrShPb").text
        endereco_escola = navegador.find_element(By.CSS_SELECTOR, ".LrzXr").text
        lista_escolas.append(colegio(nome_escola=nome_escola, endereco_escola=endereco_escola))
    except:
        print('Deu ruim')

with open('teste.csv', 'w', newline='') as csvfile:
    csv.writer(csvfile).writerow(["Nome da Escola", "Endereço"])
    for escola in lista_escolas:
        csv.writer(csvfile).writerow([escola.nome_escola, escola.endereco_escola])






