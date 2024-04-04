""" 

def fetch_data():
    url = "http://ipinfo.io/176.182.219.208?token=dd9c8e94d6c24d"
    response = requests.get(url)
    data = response.json()
    return data['country'] 

"""


import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

def find_link_review(url_site):
    anime_name = anime_name.split(" ",1)[0]
    response = requests.get(url_site)
    if response.status_code != 200:
        print("requête échouée ", response.status_code)
        return None    
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all('a', href=True)
    filtered_links = [link['href'] for link in links if anime_name in link.get_text().lower()]
    if filtered_links:
        print(filtered_links[0])
        return filtered_links[0]
    else:
        print("not found")

def search_anime():
    driver = webdriver.Chrome()
    driver.set_window_size(1900, 1000)
    driver.get("https://myanimelist.net/")
    driver.implicitly_wait(5)
    element_intercept = driver.find_elements(By.CLASS_NAME, "qc-cmp-cleanslate")
    if element_intercept:
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    div_element = driver.find_element(By.CLASS_NAME, "news-unit-right")
    first_link = div_element.find_element(By.TAG_NAME,"a")
    first_link.click()
    driver.implicitly_wait(5)
    url = driver.current_url
    driver.quit()
    return url

def find_text(url_link):
    response = requests.get(url_link)
    if response.status_code != 200:
        print("requête échouée ", response.status_code)
        return None  
    soup = BeautifulSoup(response.content, 'html.parser')
    news = soup.find("div", class_="content clearfix")
    text = news.get_text(strip=True)[:800]
    return text

url_link = search_anime()
url_text = find_text(url_link)
print(url_text)

