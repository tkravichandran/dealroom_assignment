## Essential info

- 1 pg description file that summarises the logic and code used for
  the assignment.
- will be graded based on code and thought process
- instructions in readme to run the code

Good luck and send us an email if you have any questions at
pierre@dealroom.co.


## Assignment 1 (copied from pdf)

Exercise 1: G2 Scraper

In the attachments you will find a file called
“data\_scientist\_intern\_g2\_scraper.csv”, which contains 1,350
companies. Each company has an id, name, website, short description,
address and industry.

Your task is to build a scraper for https://www.g2.com/ (G2 is a
website providing product reviews). Your script should look up the
companies from the file and return the corresponding product
information for each company.

The scraper should get the product URL
(e.g. https://www.g2.com/products/trello/reviews), website, rating,
number of reviews, description, product and seller details,
alternatives (optional) and pricing (also optional). You can save the
scraped data to the initial companies file and send it to us together
with the script you’ve built to scrape the data.

If you get blocked by G2, it’s ok, just share the results you
scraped. The point is the code and the logic.


## Assignment 1 page description

**Goal**

Scrape information from product websites from G2.

**Method and pseudo code**

1. Get search results
   1. Initial cleaning of name (to make it searchable)
   2. Open Search results directly using company name (`cname`)
   `driver.get("https://www.g2.com/search?utf8=%E2%9C%93&query="+cname)`
2. Scrape upto first 20 results and find which is the "corresponding company"
   1. Get g2-website for each of the results
   2. Search the g2-website to get company website
   3. Check if the company website matches the website from the CSV
   4. Thus identify the "right company"
   5. When there is no company or no match step 3 is skipped.
3. Extract details in `try` `except` statements **including pricing and
   alternatives** when available.
   1. For alternatives the site of alternatives is extracted from which
      all 20 of the alternatives are taken.
4. Save to pandas and eventually to CSV.

**Types of Cases to test to ensure robustness of script**

1. Search gives no results
2. Search gives results but no company website matches CSV data
3. Search gives many results and the top one matches
4. Search gives many results and one them matches
5. Additional cases where g2-website structure is different.

**Method: scraping**

- `Urllib` did not even allow me to access the website, despite
  changing the `user-agent`. Worked on other websites but not on G2.

- Using `Selenium` to navigate G2 resulted in `CAPTCHA` for every
  single page. This CAPTCHA seemed so hard that I was unable to
  solve it even with human intervention.
  
- What seems to work is *opening and closing websites directly without interacting
  with their hyperlinks*.

- Used `Selenium` as the single tool for web navigation and
  scraping along with `fake_useragent`. 
  


**Avoiding captcha and other prevention measures**

1. I was able to access websites using Selenium, but only the
  navigation was the issue.
  
  - So in order to search through the website, I directly searched

	    url = "https://www.g2.com/search?utf8=%E2%9C%93&query="+cname
		driver = open_website(url)
  - Every time I just closed and opened a new website directly and this way I
	didn't get blocked at all. No clicking on hyperlinks or search bars.
	
2. I added random times `>5s` to overcome the "DDOS Protection by
CloudFare".

**Issues**

- Slow processing (>5s only to open a file) mainly due to avoiding
  "DDOS Protection"
- Sometimes not all values are scraped as "try excepts" are not made
for every single output extracted, but for a group of outputs (but this could be done).

- There is variation in g2-product-websites accessed. Current script
is able to handle many variations but not all. Program will continue
but we might be missing some data. (Example, Company Alan gives not much
additional data as the site Xpath is considerable different.)

- Got blocked while scraping approximately 140 companies.

**Salient features**
- Able to extract alternatives and pricing when available
- Exceptions handled to keep the script going on.

<div class="fw-semibold c-midnight-100 word-break-word">Woliba</div>
**Verbose Print output for checking**

``` python
---------------------------------------------
Forecast is being searched
title is G2 Search: Forecast
Number of search results are 20
...
Looping through the different search results
Title is Forecast Reviews 2021: Details, Pricing, & Features | G2
Found match with company website from CSV @ 0 index
Getting details for Forecast
Showing more


id                                                            975908
NAME                                                        Forecast
WEBSITE                                     https://www.forecast.app
TAGLINE            AI-powered resource & project management platform
ADDRESS              20, Frederiksborggade, 1360 Copenhagen, Denmark
INDUSTRIES                                       enterprise software
TYPE                                                             NaN
current_url        https://www.g2.com/products/forecast-forecast/...
website                             https://www.forecast.app/product
rating                                                           4.3
n_reviews                                                 48 reviews
desc               Forecast is a full-suite platform for improvin...
prod_det           All-in-one Project and Portfolio Management So...
language                  Languages SupportedDanish, English, French
seller_who                                            SellerForecast
seller_location                       HQ LocationCopenhagen, Denmark
seller_year                                         Year Founded2016
pricing_lite                                       $29per seat/month
pricing_pro                                        $29per seat/month
alternatives                                    #1monday.com-#2Avaza
Name: 4, dtype: object
```

## Assignment 3 (copied from pdf)

Exercise 3: Duplicate detection In
“data_scientist_intern_duplicate_detection.csv” you will find a sample
dataset of Dealroom company data containing some duplicates. Your task
is to **identify the duplicate profiles** based on the information
provided in the file. Please **create a separate file to store the
duplicate profiles** that you identified. In this file you should show
which of the profiles (data rows) are duplicates and which fields they
are duplicated on.

## Assignment 3 1 page description

**Assumption**: Something is duplicate if the name, country and city are
the same.

1. Get df and make copy 

2. Explore the data (check Nan, unique, dtypes and duplicates for applicable
   columns)

3. Group by Name Country and City and count them

4. Add column: Join(Name country and City)

5. Filer counts>1 (i.e., duplicates)

6. Make CSV


**Other things to consider:**

Some of the companies have very similar names and could potentially be
duplicates (e.g., "3NCRYPT3D Messaging Services" and "3NCRYPT3D"). Did
not work on it this time.
