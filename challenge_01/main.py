import csv
import time
import models.school as sch
from parsel import Selector
from parsel import css2xpath

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

#Funcao para pegar uma coluna específica no .csv
def get_column_of_csv(filename, column=[]):
    with open(filename, "r", encoding='utf8') as stream:
        reader = csv.DictReader(stream, delimiter=";")
        for row in reader:
            yield row[column[0]] + ' ' + row[column[1]] + ' ' + row[column[2]]

srv = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=srv)
schl = sch.School

schools_list = []
schools_not_found = []
schools = []
keys = ["Município", "UF", "Escola"]

i = 0
for name in get_column_of_csv('./challenge_01/files/escolas_ms.csv', keys):
    schools.append(name)
    i += 1
    if(i==1):
        break
    
# Trecho de automação das pesquisas no Google
for item in schools:
    try:
        browser.get("https://www.google.com")
        browser.find_element(By.XPATH, '//*[@id="APjFqb"]').clear()
        browser.find_element(By.XPATH, '//*[@id="APjFqb"]').send_keys(item + Keys.RETURN)
        name = browser.find_element(By.CSS_SELECTOR, ".qrShPb").text
        adress = browser.find_element(By.CSS_SELECTOR, ".LrzXr").text
        telephone = browser.find_element(By.CSS_SELECTOR, '.zdqRlf').text
        schools_list.append(schl(name=name, adress=adress, telephone=telephone))
        #time.sleep(3)
    except:
        name = browser.find_element(By.XPATH, '//*[@id="APjFqb"]').text
        schools_not_found.append(name)

# Aqui salva o array das buscas realizadas com sucesso
with open('challenge_01/files/base_nova.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csv.writer(csvfile).writerow(["Nome da Escola", "Endereço", "Telefone", "Status"])
    for item in schools_list:
        csv.writer(csvfile).writerow([item.name, item.adress, item.telephone])
        
# Aqui salva o array das buscas sem sucesso
with open('challenge_01/files/escolas_nao_salva.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csv.writer(csvfile).writerow(["Nome da Escola"])
    for item in schools_not_found:
        csv.writer(csvfile).writerow([item])

# Lógica de busca no Google Maps das escolas encontradas (dados mocados)
browser.get("https://www.google.com.br/maps/search/escolas+publicas+em+tres+lagoas+ms/@-20.7735345,-51.715064,15z/data=!3m1!4b1?entry=ttu")
page_content = browser.page_source
response = Selector(page_content)

css2xpath('div.Nv2PK')
results = response.xpath("descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' Nv2PK ')]")

for item in results:
    print(item.attrib.get('aria-label'))