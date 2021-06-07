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

############################# Definitions of functions #############

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
    # Open the website on chrome
    driver = webdriver.Chrome(options=options,
                          executable_path=path)
    driver.get(url)

    time.sleep(uniform(6,11))# sleep for random time before clicking
    print("Title is:  ", driver.title)

    #Accept cookies
    try:
        driver.find_element_by_xpath(
            "//input[@value='I accept all cookies']").click()
    except Exception as e:
        print("Exception while accepting cookies", repr(e))
        
    return driver

#Initialize the variables in the dictionary to empty
def initialize_output():

    var_lst = ["current_url", "website","alt_website","rating","n_reviews","desc",
                "prod_det", "language", "seller_who",
                "seller_location", "seller_year", "pricing_lite",
                "pricing_pro"
                ,"alternatives"]
    return dict.fromkeys(var_lst,"")

# Extract the different sites from the search Results
def extract_g2_sites(driver):
    
    search_results = []
    url_g2s = []
    url_g2s_alt = []
    try:
        search_results = WebDriverWait(driver, 5).until(lambda x:
                            x.find_elements_by_xpath("//div[@class='paper mb-1']"))
        #print("number of results are", len(search_results))
    except Exception as e:
        print("Exception while finding search results", repr(e))
    
    if len(search_results)>0:
        for result in search_results:
            # Get link to reviews
            url_g2s.append(result.find_element_by_link_text(
                "Reviews").get_attribute("href"))
            # Get link to alternatives
            url_g2s_alt.append(result.find_element_by_link_text(
                "Alternatives").get_attribute("href"))
            
    print(url_g2s,url_g2s_alt)
    return url_g2s,url_g2s_alt

# Extract company website from the g2 reviews site
def get_company_website_from_g2_site(url):

    driver = open_website(url)
    #print(driver.current_url)
    c_website_g2 = driver.find_element_by_xpath("//a[@class='link']").get_attribute("href")

    return c_website_g2, driver

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
    except Exception as e:
        print("Exception in basics")
        print("Exception is", repr(e))

    try:    
        # website
        output["website"] = driver_c.find_element_by_xpath("//a[@class='link']").get_attribute("href")
        #description
        output["desc"] = driver_c.find_element_by_xpath(
            "//div[@class='ws-pw']").get_attribute("textContent")
    except Exception as e:
        print("Exception in website and description")
        print("Exception is", repr(e))
        
    # Click show more to unlock other Product and Seller details
    try:
        show_more = driver_c.find_element_by_xpath(
            "//*[@id='leads-sticky-top']/div/div[1]/div[3]/div[1]/div[2]/a")
        
        actions = ActionChains(driver_c)
        actions.move_to_element(show_more).perform()
        
        show_more.click()
        time.sleep(2.5)
        print("Clicking to show more")
    except Exception as e:
        print("exception in showmore")
        print("Exception is", repr(e))
        
    # Product and Seller details
    try:
        output["prod_det"] = driver_c.find_element_by_xpath(
            "//div[@class='p-1 border-top']/div[@class='js-show-more-detail']/p").get_attribute("textContent")
        
        output["language"] = driver_c.find_element_by_xpath(
            "//div[@class='grid-x']/div[2]").get_attribute("textContent")
        
        output["seller_who"] = driver_c.find_element_by_xpath(
            "//*[@id='leads-sticky-top']/div/div[1]/div[3]/div[1]/div[2]/div[4]/div[2]/div[1]/div[1]/div/div").get_attribute("textContent")
        
        output["seller_location"] = driver_c.find_element_by_xpath("//*[@id='leads-sticky-top']/div/div[1]/div[3]/div[1]/div[2]/div[4]/div[2]/div[2]/div[1]/div/div").get_attribute("textContent")
        
        output["seller_year"] = driver_c.find_element_by_xpath(
            "//*[@id='leads-sticky-top']/div/div[1]/div[3]/div[1]/div[2]/div[4]/div[2]/div[1]/div[3]/div/div").get_attribute("textContent")
    except Exception as e:
        print("Exception in product and seller data")
        print("Exception is", repr(e))   
    # pricing (optional)
    try:
        output["pricing_lite"] = driver_c.find_element_by_xpath("//*[@id='leads-sticky-top']/div/div[2]/div[1]/div/div[1]/div[1]/a[1]/div[2]").get_attribute("textContent")
        
        output["pricing_pro"] = driver_c.find_element_by_xpath("//*[@id='leads-sticky-top']/div/div[2]/div[1]/div/div[1]/div[1]/a[1]/div[2]").get_attribute("textContent")
    except Exception as e:
        print("Exception in pricing")
        print("Exception is", repr(e))

## get_alternatives
def get_alternatives(url_alt,output):

    output["alt_website"]=url_alt
    try:
        driver = open_website(url_alt)
        alts = driver.find_elements_by_css_selector("div.product-listing--competitor.x-ordered-events-initialized")
        #print(alts)
        alt_lst =[]
        for alt in alts:
            temp = alt.get_attribute("textContent")
            temp = temp[:temp.find("(")] # scrape the part that is necessary
            #temp = alt.find_element_by_xpath("//div[@itemprop='name']").get_attribute("textContent")
            #print(alt.get_attribute("textContent")) # doesn't work for some reason
            print(temp)
            alt_lst.append(temp)
        output["alternatives"]= "-".join(alt_lst)
        
    except Exception as e:
        print("Exception due to alternatives",repr(e))
    finally:
        driver.close()

######################################## Main ###############
#######################################        ##############

# Set options to "make it hard for the website to detect"
options = Options()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument(f'user-agent={userAgent}')

path = "../dater/driver/chromedriver"

# Get the data into pandas
df_t = pd.read_csv("data_scientist_intern_g2_scraper.csv")
df = df_t.copy()

# Choosing range from CSV to extract
row_lst = [8,9,10] #list(range(200))#[3,0,4,10,8]#randint(0,100)
start = time.time()

# running the loop over all names
for i in row_lst:
    found_match_flag=False
    # Starting with basic info on company from CSV
    print("\n\n\n")
    print("-"*45)
    print(i,"th iteration going on")
    cname = clean_name(df.NAME[i])
    print(cname, "is being searched")
    c_website = df.WEBSITE[i]
    

    # 1. Search and get search results
    url = "https://www.g2.com/search?utf8=%E2%9C%93&query="+cname
    driver = open_website(url)
    url_g2_sites,url_g2_sites_alt = extract_g2_sites(driver)

    print("Number of search results are", len(url_g2_sites) )
    print(url_g2_sites)# search results
    print("\n")
    driver.close(); time.sleep(1)

    # 2. Loop through search results and find if there are matching sites
    if not url_g2_sites:
        print("Found No Results")
        found_match_flag=False
        
    print("Looping through the different search results")
    for url_g2 in url_g2_sites[0:5]:

        # open search result website and extract company website
        c_website_g2, driver_c = get_company_website_from_g2_site(url_g2)

        # Clean and check if csv website is a MATCH
        c_website_clean = clean_c_website(c_website)
        if re.search(c_website_clean,c_website_g2):
            which_index = url_g2_sites.index(url_g2) #get index
            print("Found match with company website from CSV @",
                  which_index)
            found_match_flag=True
            break

        # if it doesn't find a match it closes
        driver_c.close()
        time.sleep(1.35)

        if url_g2==url_g2_sites[-1]:
            print("Found no match with company website from CSV")
            found_match_flag=False
            
    # 3. Extract basic details from driver.c
    output = initialize_output()
    if found_match_flag:
        print("Getting details for company", cname)
        get_details(driver_c, output)
        print("\nGetting Alternatives details")
        get_alternatives(url_g2_sites_alt[which_index], output)
    
    # 4. add to pandas (not th emost efficient way)
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
df.to_csv("assign1-200.csv", index=False)



        
