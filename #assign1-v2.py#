
## Import 
import pandas as pd
import numpy as np

## Import for website manipulation
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from selenium.webdriver.common.touch_actions.TouchActions import
scroll
from selenium.webdriver.common.action_chains import ActionChains

import time
from random import randint,uniform
import re
from urllib.parse import urlparse


## Get the data into pandas
df_t = pd.read_csv("data_scientist_intern_g2_scraper.csv")
df = df_t.copy()

print(df.NAME[0], "has 0 cases")
print(df.NAME[4],
      "has many cases but is the first option. with website:",
      df.WEBSITE[4])

print(df.NAME[8],
      "has many cases, but none of them match the website:",
      df.WEBSITE[4])

## Choosing for testing
n=10#randint(0,100)
cname = df.NAME[n]
c_website = df.WEBSITE[n]

## cleaning the name
cname = re.sub(" \(.*\)", "", cname)# remove brackets
cname = cname.replace(" ","+")# add + to make the search easy
print("cleaned name is", cname)

## Set options to "make it hard for the website to detect"
## But still I get blocked if I try to use another VPN or anything
## as long as I do something on the website.
options = Options()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument(f'user-agent={userAgent}')

path = "../dater/driver/chromedriver"

## Searching directly and accept cookies
url = "https://www.g2.com/search?utf8=%E2%9C%93&query="+cname
print(url)

def open_website(url):

    driver = webdriver.Chrome(chrome_options=options,
                          executable_path=path)
    driver.get(url)

    time.sleep(uniform(5,20))# sleep for random time before clicking
    print("title is", driver.title)

    driver.find_element_by_xpath(
    "//input[@value='I accept all cookies']").click()# accept the
    # cookies

    return driver

driver = open_website(url)

## extract info on number of items, hyperlink

def extract_g2_sites(driver):
    
    results=[]
    results = WebDriverWait(driver, 10).until(lambda x:
                x.find_elements_by_xpath("//div[@class='paper mb-1']"))

    print("number of results are", len(results))
    url_g2s = []
    if len(results)>0:
        for result in results:
            url_g2s.append(result.find_element_by_link_text(
                "Reviews").get_attribute("href"))
    print(url_g2s)
    return url_g2s

url_g2s = extract_g2_sites(driver) 

## compare with website name if we have the right company
url_g2s= ["https://www.g2.com/products/unmind/reviews",
         "https://www.g2.com/products/forecast-forecast/reviews"]

def get_company_website_from_g2_site(url):

    driver = open_website(url)
    print(driver.current_url)
    c_website_g2 = driver.find_element_by_xpath("//a[@class='link']").get_attribute("href")

    return c_website_g2, driver
    
c_website_g2, driver_c = get_company_website_from_g2_site(url_g2s[1])
c2 = c_website
print(c1,c2)

def clean_c_website(o):
    return urlparse(re.sub("www.","",o))[1]

print(clean_c_website(c_website_g2) == clean_c_website(c_website))
print(re.search(clean_c_website(c_website),c_website_g2))

current_url = driver_c.current_url
print(current_url)
rating = driver_c.find_element_by_xpath(
    "//span[@class='fw-semibold']").get_attribute("textContent")
print(rating)

n_reviews = driver_c.find_element_by_xpath(
    "//div[@class='star-wrapper__desc']").get_attribute("textContent")
print(n_reviews)

desc = driver_c.find_element_by_xpath(
    "//div[@class='ws-pw']").get_attribute("textContent")
print(desc)

## other deails are hidden under "show more"

show_more = driver_c.find_element_by_xpath(
    "//*[@id='leads-sticky-top']/div/div[1]/div[3]/div[1]/div[2]/a")

actions = ActionChains(driver_c)
actions.move_to_element(show_more).perform()

show_more.click()

time.sleep(5)
prod_det = driver_c.find_element_by_xpath(
    "//div[@class='p-1 border-top']/div[@class='js-show-more-detail']/p").get_attribute("textContent")#?
print(prod_det)
language =  driver_c.find_element_by_xpath(
    "//div[@class='grid-x']/div[2]").get_attribute("textContent")
print(language)
seller_who = driver_c.find_element_by_xpath(
    "//*[@id='leads-sticky-top']/div/div[1]/div[3]/div[1]/div[2]/div[4]/div[2]/div[1]/div[1]/div/div").get_attribute("textContent")
print(seller_who)
seller_location = driver_c.find_element_by_xpath("//*[@id='leads-sticky-top']/div/div[1]/div[3]/div[1]/div[2]/div[4]/div[2]/div[2]/div[1]/div/div").get_attribute("textContent")
print(seller_location)
seller_year = driver_c.find_element_by_xpath("//*[@id='leads-sticky-top']/div/div[1]/div[3]/div[1]/div[2]/div[4]/div[2]/div[1]/div[3]/div/div").get_attribute("textContent")
print(seller_year)

## Pricing put it under try

pricing_lite = driver_c.find_element_by_xpath("//*[@id='leads-sticky-top']/div/div[2]/div[1]/div/div[1]/div[1]/a[1]/div[2]").get_attribute("textContent")
print(pricing_lite)
pricing_pro = driver_c.find_element_by_xpath("//*[@id='leads-sticky-top']/div/div[2]/div[1]/div/div[1]/div[1]/a[2]/div[2]").get_attribute("textContent")
print(pricing_pro)

## alternatives put it in try

alternatives = driver_c.find_elements_by_class_name("compare-list__texts")
alternative = alternatives[0].get_attribute("textContent")
print(alternative)



#driver.close()
