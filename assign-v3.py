# Import 
import pandas as pd
import numpy as np

# Import for website manipulation
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.common.touch_actions.TouchActions import scroll
from selenium.webdriver.common.action_chains import ActionChains

from fake_useragent import UserAgent
import time
from random import randint,uniform
import re
from urllib.parse import urlparse

start = time.time()
# Set options to "make it hard for the website to detect" But still I
# get blocked even if I try to use another VPN or anything as long as
# I do something on the website.
options = Options()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument(f'user-agent={userAgent}')

path = "../dater/driver/chromedriver"

# Get the data into pandas
df_t = pd.read_csv("data_scientist_intern_g2_scraper.csv")
df = df_t.copy()

print(df.NAME[0], "has 0 working cases")
print(df.NAME[4],
      "has many cases but is the first option with website:",
      df.WEBSITE[4])

print(df.NAME[8],
      "has many cases, but none of them match the website:",
      df.WEBSITE[8])

print(df.NAME[10],
      "has 1 cases, but is the first option with te:",
      df.WEBSITE[10])

print(df.NAME[3],
      "has 1 cases, but is the first option with te:",
      df.WEBSITE[3])

# Cleaning the name
def clean_name(cname):
    cname = re.sub(" \(.*\)", "", cname)# remove brackets and # characters in it
    cname = cname.replace(" ","+")# add + to make the search proper
    #print("cleaned name is", cname)
    return cname

# Cleaning the website to check matches
def clean_c_website(o):
    return urlparse(re.sub("www.","",o))[1]

# Search url and accept cookies
def open_website(url):

    driver = webdriver.Chrome(options=options,
                          executable_path=path)
    driver.get(url)

    time.sleep(uniform(5,20))# sleep for random time before clicking
    print("title is", driver.title)

    try:
        driver.find_element_by_xpath(
            "//input[@value='I accept all cookies']").click()
    except Exception as e:
        print("Exception while accepting cookies", repr(e))
        
    return driver


def initialize_output():
    var_lst = ["current_url", "website","rating","n_reviews","desc",
                "prod_det", "language", "seller_who",
                "seller_location", "seller_year", "pricing_lite",
                "pricing_pro"
                ,"alternatives"]
    return dict.fromkeys(var_lst,"")

# Extract the different sites from the search
def extract_g2_sites(driver):
    
    search_results = []
    url_g2s = []
    try:
        search_results = WebDriverWait(driver, 5).until(lambda x:
                            x.find_elements_by_xpath("//div[@class='paper mb-1']"))
        #print("number of results are", len(search_results))
    except Exception as e:
        print("Exception while finding search results", repr(e))
    
    if len(search_results)>0:
        for result in search_results:
            url_g2s.append(result.find_element_by_link_text(
                "Reviews").get_attribute("href"))
    #print(url_g2s)
    return url_g2s

def get_company_website_from_g2_site(url):

    driver = open_website(url)
    #print(driver.current_url)
    c_website_g2 = driver.find_element_by_xpath("//a[@class='link']").get_attribute("href")

    return c_website_g2, driver

# # get text from xpath
# def get_text_from_xpath(driver_c,xpath):
#     driver_c.find_element_by_xpath(
#         xpath).get_attribute("textContent")

# Gets all deatils necessary
def get_details(driver_c,output):
    
    try:
        # current_url
        output["current_url"] = driver_c.current_url
        
        # rating
        output["rating"] = driver_c.find_element_by_xpath(
            "//span[@class='fw-semibold']").get_attribute("textContent")
        
        # n_reviews
        output["n_reviews"] = driver_c.find_element_by_xpath(
            "//div[@class='star-wrapper__desc']").get_attribute("textContent")
        
        # website
        output["website"] = driver_c.find_element_by_xpath("//a[@class='link']").get_attribute("href")
        #description
        output["desc"] = driver_c.find_element_by_xpath(
            "//div[@class='ws-pw']").get_attribute("textContent")
        
        # show more to unlock other details
        show_more = driver_c.find_element_by_xpath(
            "//*[@id='leads-sticky-top']/div/div[1]/div[3]/div[1]/div[2]/a")
        
        actions = ActionChains(driver_c)
        actions.move_to_element(show_more).perform()
        
        show_more.click()
        time.sleep(2.5)
        print("showing more")
        # product details
        output["prod_det"] = driver_c.find_element_by_xpath(
            "//div[@class='p-1 border-top']/div[@class='js-show-more-detail']/p").get_attribute("textContent")
        
        output["language"] = driver_c.find_element_by_xpath(
            "//div[@class='grid-x']/div[2]").get_attribute("textContent")
        
        output["seller_who"] = driver_c.find_element_by_xpath(
            "//*[@id='leads-sticky-top']/div/div[1]/div[3]/div[1]/div[2]/div[4]/div[2]/div[1]/div[1]/div/div").get_attribute("textContent")
        
        output["seller_location"] = driver_c.find_element_by_xpath("//*[@id='leads-sticky-top']/div/div[1]/div[3]/div[1]/div[2]/div[4]/div[2]/div[2]/div[1]/div/div").get_attribute("textContent")
        
        output["seller_year"] = driver_c.find_element_by_xpath(
            "//*[@id='leads-sticky-top']/div/div[1]/div[3]/div[1]/div[2]/div[4]/div[2]/div[1]/div[3]/div/div").get_attribute("textContent")
        
        # pricing (optional)
        output["pricing_lite"] = driver_c.find_element_by_xpath("//*[@id='leads-sticky-top']/div/div[2]/div[1]/div/div[1]/div[1]/a[1]/div[2]").get_attribute("textContent")
        
        output["pricing_pro"] = driver_c.find_element_by_xpath("//*[@id='leads-sticky-top']/div/div[2]/div[1]/div/div[1]/div[1]/a[1]/div[2]").get_attribute("textContent")

        # Alternatives
        alts = driver_c.find_elements_by_class_name("compare-list__texts")
        alt_lst = []
        for alt in alts:
            alt_lst.append(alt.get_attribute("textContent"))
        output["alternatives"] = "-".join(alt_lst)
        
    except Exception as e:
        print("Exception is", repr(e))
 

# Choosing for testing
row_lst = list(range(0,10))#[3,0,4,10,8]#randint(0,100)

# running the loop over all names
for i in row_lst:
    print("\n\n\n")
    print("-"*30)
    cname = clean_name(df.NAME[i])
    print(cname, "is being searched")
    c_website = df.WEBSITE[i]
    

    # Unable to use the search bar as it leads to captcha which even
    # as a human I am unable to solve :( So this way no captcha is
    # involved.
    url = "https://www.g2.com/search?utf8=%E2%9C%93&query="+cname
    driver = open_website(url)
    url_g2_sites = extract_g2_sites(driver)
    print("Number of search results are", len(url_g2_sites) )
    print(url_g2_sites)
    print("\n")
    driver.close(); time.sleep(1)
    
    # Loop through url_g2_sites and find if there are matching sites
    # then get details
    print("Looping through the different search results")
    if not url_g2_sites:
        print("Found No Results")
    for url_g2 in url_g2_sites:
        c_website_g2, driver_c = get_company_website_from_g2_site(url_g2)
        c_website_clean = clean_c_website(c_website)

        if re.search(c_website_clean,c_website_g2):
            print("found match with company website from CSV @",
            url_g2_sites.index(url_g2),"index")
            break
        
        driver_c.close()# if it doesn't find a match it closes
        time.sleep(1.35)

        if url_g2==url_g2_sites[-1]:
            print("Found no match with company website from CSV")
            
    # Extract basic details from driver.c
    print("getting details for", cname)
    output = initialize_output()
    if url_g2_sites: get_details(driver_c, output)
    
    #add to pandas (not th emost efficient way)
    df.loc[i,list(output.keys())] = list(output.values())
    print("\n")
    print(df.loc[i])
    
    # Close all
    try:
        driver_c.close()
        time.sleep(1.35)
    except:
        pass

    #print(output)
    
end=time.time()
print(end-start)


