# to access the html content of a single property url
from typing import Self
import requests 

# to select parts of an XML or HTML using BeautifulSoup
from bs4 import BeautifulSoup 

# to use regular expressions
import re 

# to build a dictionary form a string
import json

# to run the sleep method
import time

# We use Selenium as we are scraping a webpage which uses javascript
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait # Used to add a wait condition
from selenium.webdriver.support import expected_conditions as EC # used to add a wait condition

# Shadow roots, don't know which package we actually need
from selenium.webdriver.remote.command import Command # First package to deal with shadow roots
from selenium.webdriver.remote.shadowroot import ShadowRoot # Second package to deal with shadow roots

class HouseApartmentScraping():
    
    def __init__(self):
        self.root_url = "https://www.immoweb.be/en/search/house/for-sale?countries=BE"
              
        #self.house_dict = house_dict()
        
       # self.property_ID = property_ID()
       # self.locality_name = self.locality_name()
       # self.postal_code = self.postal_code()
        # self.price = self.price()
        #self.type_property = self.type_property()
        #self.subtype = self.subtype()
        #self.type_sale = self.type_sale()
        #self.num_rooms = self.num_rooms()
        #self.living_area = self.living_area()
        #self.equipped_kitchen = self.equipped_kitchen()
        #self.furnished = self.furnished()
        #self.open_fire = self.open_fire()
        #self.terrace_area = self.terrace_area()
        #self.garden_area = self.garden_area()
        #self.surface_good = self.surface_good()
        #self.num_facade = self.num_facade()
        #self.pool = self.pool()
        #self.state = self.state()
        self.property_info = {}


    def listing_list(self, url, soup):
        """Method for extracting the following information of the house: property ID, postcode, price, living area.
        """
        html = requests.get(self.url).content
        soup = BeautifulSoup(html,'html.parser')
        listings = []
        for listing in soup:
            for elem in soup.find_all("li", attrs = {"class":"search-results__item"}):
                listing = elem.get("href")
                listings.append(listing)


    def first_details(self,url):
        html = requests.get(url).text
        soup = BeautifulSoup(html,'html.parser')
        print(soup,type(soup))
        #for elem in soup.find_all("div", attrs = {"class":"classified__header--immoweb-code"}):
        #    self.property_info["Property_ID"] = elem
        for elem2 in soup.find_all("span", attrs = {"class":"classified__information--address-row"}):
            print(elem2)
       # print(self.property_info)
            
        #for elem in soup.find_all()   
            

    def get_details(self, url):
        '''Method to extract Postal Code from Immoweb using Selenium'''

        options = webdriver.ChromeOptions() 
        options.add_argument("--auto-open-devtools-for-tabs")
        options.add_experimental_option("detach", True)

        driver = webdriver.Chrome(options=options)
        driver.get(url)

        time.sleep(5)

        element = driver.execute_script("""return document.querySelector('#usercentrics-root').shadowRoot.querySelector('div div div div div div div div div div div button[data-testid="uc-accept-all-button"]')""")
        element.click()

        driver.maximize_window()

        postal_code = driver.find_elements(By.XPATH, "//span[@class='classified__information--address-row']")
        th_tags_keys = driver.find_elements(By.XPATH, "//tbody[@class='classified-table__body']//th")
        td_tags_values = driver.find_elements(By.XPATH, "//tbody[@class='classified-table__body']//td")

        tag_keys = [i.text for i in th_tags_keys]
        tag_values = [i.text for i in td_tags_values]
        postal_code_text = [i.text for i in postal_code]


        print(tag_keys)
        print(tag_values)
        print(postal_code_text)



    def remove_duplicates(self, filepath):
        pass


    def clean_data(self, filepath):
        pass


    def remove_empty_rows(self, filepath):
        pass


    #def to_csv(self, filepath):
      #with open('../csv_files/houses_apartments_urls.csv', 'w') as file:
          #for page_url in houses_url:
              #pass
          #for url in page_url:
              #file.write(url+'\n')
        
                
  