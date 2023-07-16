from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import pandas as pd

url = "https://www.tokopedia.com/dellflagship/review"
driver = webdriver.Chrome()
driver.maximize_window()
driver.get(url)
time.sleep(3)

data_ulasan=[]
data_rating=[]
for i in range(0,10):
    bs = BeautifulSoup(driver.page_source, "html.parser")
    container = bs.findAll('article', attrs={'class' : 'css-ccpe8t'})
    
    for c in container:
        rating = c.find('div', attrs={'data-testid' : 'icnStarRating'})['aria-label']
        rating2 = rating.replace("bintang ", "")
        print(rating2)
        data_rating.append((rating2))
        
        ulasan_elem = c.find('span', attrs={'data-testid' : 'lblItemUlasan'})
        if ulasan_elem is not None and ulasan_elem.text.strip() != "":
            ulasan = ulasan_elem.text
            print(ulasan)
            data_ulasan.append((ulasan))
        
    time.sleep(2)
    tombol_next = WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH, "//button[@aria-label='Laman berikutnya']")))
    tombol_next.click()
    time.sleep(3)
    
df_ulasan = pd.DataFrame(data_ulasan, columns=['Ulasan'])
print(df_ulasan)

df_rating = pd.DataFrame(data_rating, columns=['Rating'])
print(df_rating)

data_gabung = pd.concat([df_ulasan, df_rating], axis=1)
print(data_gabung)
data_gabung.to_csv("ulasan_tokopedia_dellstore.csv", sep=';', index=False)

    
