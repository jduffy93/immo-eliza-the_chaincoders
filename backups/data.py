# to access the html content of a single property url
import requests 

# to select parts of an XML or HTML text using CSS or XPath and extract data from it
from parsel import Selector 

import time

# 1) Obtain 10000 url of houses with webdriver (appartments below)

driver = webdriver.Chrome()

# The url of each house that resulted from the search will be stored in the "houses_url" list.
houses_url = []

# Iterate through all result pages (i) and get the url of each of them
for i in range(1, 2):
    apikey = str(i)+'&orderBy=relevance'
    url = 'https://www.immoweb.be/en/search/house/for-sale?countries=BE&page='+apikey

    # An implicit wait tells WebDriver to poll the DOM for a
    #  certain amount of time when trying to find any element 
    #     (or elements) not immediately available. 
    time.sleep(10)
    
    # The first thing you’ll want to do with WebDriver is navigate
    #   to a link. The normal way to do this is by calling get method:    
    driver.get(url)