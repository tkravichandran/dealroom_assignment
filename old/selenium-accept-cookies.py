
## Import 
import pandas as pd
import numpy as np

## Get the data into pandas
df_t = pd.read_csv("data_scientist_intern_g2_scraper.csv")
# print(df_t.columns)
# print(df_t.head)

df = df_t.copy()



## waiting

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from random import randint,uniform

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Set options
from fake_useragent import UserAgent

options = Options()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument(f'user-agent={userAgent}')

cname= "Unmind"
urlg2shift = "https://www.g2.com/products/"+cname+"/reviews"
urlg2 = "https://www.g2.com/"
url2 = "https:\\techwithtim.net"
urlfb = "https://www.facebook.com/"
urlinptest="https://www.g2.com/products/trade-republic/reviews"

## Driver setup and access title

path = "../dater/driver/chromedriver"
driver = webdriver.Chrome(chrome_options=options, executable_path=path)
driver.get(urlg2shift)
time.sleep(uniform(5,20))
print("title is", driver.title)

## Accept the fucking cookies
element1 = driver.find_element_by_xpath("//input[@value='I accept all cookies']").click()


## xpath format as `//tag[@anythingintag=value]`

## Extracting dater from websites

print(driver.current_url)
link = driver.find_element_by_xpath("//a[@class='link'][text()='Unmind']").get_attribute("href")
print(link)


rating =driver.find_element_by_xpath("//span[@class='fw-semibold']").get_attribute("textContent")
print(rating) ## please get the top element first and then the rest

## setting rules after a search function...

## Search

search = driver.find_element_by_name("query")#"query"
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

