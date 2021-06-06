
## Import 
import pandas as pd
import numpy as np

## Get the data into pandas
df_t = pd.read_csv("data_scientist_intern_g2_scraper.csv")
# print(df_t.columns)
# print(df_t.head)

df = df_t.copy()

name = "unmind"

## waiting

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from random import randint

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://www.g2.com/products/shift/reviews"
url3 = "https://www.g2.com/"
url2 = "https:\\techwithtim.net"

## Driver setup and access title

path = "../dater/driver/chromedriver"
driver = webdriver.Chrome(path)
driver.get(url2)
time.sleep(randint(5,10))
#driver.close() # to just close the tab
print("title is", driver.title)

## Search

search = driver.find_element_by_name("s")#"query"
search.send_keys("test")
search.send_keys(Keys.RETURN)

#time.sleep(randint(5,20))

## Extract main from the new page and then headers

try:
    main = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "main"))
    )
    
    #print(main.text)
    header=[]
    articles = main.find_elements_by_tag_name("article")
    for article in articles:
        header.append(article.find_element_by_tag_name("a").get_attribute("textContent"))#text)
    print(header)
except:
    driver.quit()

## find and click element


#element1 = main.find_element_by_link_text("November 4, 2019")
element1 = articles[0].find_element_by_tag_name("a")
element1.click()

# element = WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.ID, "main"))

#driver.quit() # to close everything

