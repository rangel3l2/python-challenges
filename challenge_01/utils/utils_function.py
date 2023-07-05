import csv
import time
import models.school as sch
import utils.utils_function as utils
from parsel import Selector
from parsel import css2xpath

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException

srv = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=srv)
schl = sch.School

path_to_csv = "./challenge_01/files/"
schools_list = []
schools_not_found = []
schools = []
keys = ["Escola", "Município", "UF"]
ximbinha = []
   
def get_column_of_csv(filename, column=[]):
    with open(filename, "r", encoding='utf8') as stream:
        reader = csv.DictReader(stream, delimiter=";")
        for row in reader:
            yield row[column[0]] + ' ' + row[column[1]] + ' ' + row[column[2]]

def get_column_of_csv(filename, column1, column2):
    with open(filename, "r", encoding='utf8') as stream:
        reader = csv.DictReader(stream, delimiter=",")
        for row in reader:
            yield row[column1] + ' ' + row[column2]
            
def google_search():
    i = 0
    for name in get_column_of_csv('./challenge_01/files/base_escolas_inep.csv', keys):
        schools.append(name)
        i += 1
        if(i==1):
            break
        
    for item in schools:
        try:
            browser.get("https://www.google.com")
            browser.find_element(By.XPATH, '//*[@id="APjFqb"]').clear()
            browser.find_element(By.XPATH, '//*[@id="APjFqb"]').send_keys(item + Keys.RETURN)
            name = browser.find_element(By.CSS_SELECTOR, ".qrShPb").text
            adress = browser.find_element(By.CSS_SELECTOR, ".LrzXr").text
            telephone = browser.find_element(By.CSS_SELECTOR, '.zdqRlf').text
            schools_list.append(schl(name=name, adress=adress, telephone=telephone))
            time.sleep(3)
        except:
            name = browser.find_element(By.XPATH, '//*[@id="APjFqb"]').text
            schools_not_found.append(name)

def generate_csv():
    with open('challenge_01/files/escolas_brasil_att.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv.writer(csvfile).writerow(["Nome da Escola", "Endereço", "Telefone", "Status"])
        for item in schools_list:
            csv.writer(csvfile).writerow([item.name, item.adress, item.telephone])
            
    with open('challenge_01/files/escolas_nao_salva.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv.writer(csvfile).writerow(["Nome da Escola"])
        for item in schools_not_found:
            csv.writer(csvfile).writerow([item])
                    
def extract_info_by_maps_google():
    page_content = browser.page_source
    response = Selector(page_content)

    css2xpath('div.Nv2PK')
    results = response.xpath("descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' Nv2PK ')]")

    with open(path_to_csv + 'schools_found_google_maps.csv', 'a', newline='', encoding='utf8') as csvfile:
        for item in results:
            csv.writer(csvfile).writerow([item.attrib.get('aria-label')])
            
def find_in_maps_google():
    ximbinha = get_column_of_csv("./challenge_01/files/municipios.csv", keys[1], keys[2])
    j = 0
    browser.get("https://www.google.com/maps")
    
    for item in ximbinha:
        browser.find_element(By.ID, "searchboxinput").send_keys("escolas públicas em " + item + Keys.RETURN)
        time.sleep(2)
        coluna_escolas = browser.find_element(By.XPATH, "/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]")

        while (NoSuchElementException): 
            try:
                if not(browser.find_element(By.CSS_SELECTOR, ".HlvSq") is None):
                    extract_info_by_maps_google()
                    break
            except NoSuchElementException:
                coluna_escolas.send_keys(Keys.END)
                time.sleep(2)
            
        browser.find_element(By.ID, "searchboxinput").clear()
        
        j += 1
        if (j==2):
            break