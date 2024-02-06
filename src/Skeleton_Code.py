# to access the html content of a single property url
from typing import Self
import requests 

# to select parts of an XML or HTML using BeautifulSoup
from bs4 import BeautifulSoup 

# to use regular expressions
import re 

# to build a dictionary form a string
import json 

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

    def house_dict(self):
        '''
        Define a method that creates the dictionary with attributes as keys and houses' values as values
        '''
        try:
            # The relevant info is under a "script" tag in the website
            result_set = self.soup.find_all('script',attrs={"type" :"text/javascript"})
            
            # Iterate through the "script" tags found and keep the one containing the substring "window.classified"
            # which contains all the relevant info
            for tag in result_set:
                if 'window.classified' in str(tag.string):
                    window_classified = tag
                    # when we've found the right tag we can stop the loop earlier
            
            
            # Access to the string attribute of the tag and remove leading and trailing whitespaces (strip)break
            wcs = window_classified.string
            wcs.strip()
            
            # Keep only the part of the string that will be converted into a dictionary
            wcs = wcs[wcs.find("{"):wcs.rfind("}")+1]
            
            # Convert it into a dictionary through json library
            house_dict = json.loads(wcs)
            return house_dict
        except:
            return None
        

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
        print(soup)
        #for elem in soup.find_all("div", attrs = {"class":"classified__header--immoweb-code"}):
        #    self.property_info["Property_ID"] = elem
        for elem2 in soup.find_all("span", attrs = {"class":"classified__information--address-row"}):
            print(elem2)
       # print(self.property_info)
            
        #for elem in soup.find_all()   
            

    def get_details(self, url):
        '''Method to extract Postal Code from Immoweb using Selenium'''

        driver = webdriver.Chrome() # Using Chrome because apparently Firefox has issues when it comes to shadow roots
        #wait = WebDriverWait(driver, 10) # Testing first way to solve error
        driver.get(url)
        #shadow = Command().GET_SHADOW_ROOT

        #driver.implicitly_wait(10) # Testing secondway to solve error
        #wait.until(EC.presence_of_element_located((By.XPATH, "//div[@data-testid='uc-accept-all-button']")))

        shadow_host = driver.find_element(By.ID, "usercentrics-root")
        shadow_root = shadow_host.shadow_root

        cookie_button = shadow_root.find_element(By.CSS_SELECTOR, "#uc-accept-all-button") # <- Error occurs here
        #cookie_button = driver.find_element(By.XPATH, "//div[@data-testid='uc-accept-all-button']")
        cookie_button.click()



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