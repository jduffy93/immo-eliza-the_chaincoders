# to access the html content of a single property url
from typing import Self
import requests 

# to select parts of an XML or HTML using BeautifulSoup
from bs4 import BeautifulSoup 

# to use regular expressions
import re 

# to build a dictionary form a string
import json 

import re

# We use Selenium as we are scraping a webpage which uses javascript
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait # Used to add a wait condition
from selenium.webdriver.support import expected_conditions as EC # used to add a wait condition

# Shadow roots, don't know which package we actually need
from selenium.webdriver.remote.command import Command # First package to deal with shadow roots
from selenium.webdriver.remote.shadowroot import ShadowRoot # Second package to deal with shadow roots

class Scraper():
    
    def __init__(self, url):
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
        #print(soup)
        import re
    
        for elem in soup.find_all("div", attrs={"class": "classified__header--immoweb-code"}):
            self.property_info["Property_ID"] = re.sub(r'\D', '', elem.text.strip())  # Extract only digits
        
        for elem2 in soup.find_all("span", attrs={"class": "classified__information--address-row"}):
            self.property_info["Postal_Code"] = re.sub(r'\D', '', elem2.text.strip())  # Extract only digits
        
        for elem3 in soup.find_all("td", attrs={"class": "classified-table__header"}):
            self.property_info["Living_area"] = re.sub(r'\D', '', elem3.text.strip())  # Extract only digits
        
        print(self.property_info)
        
    def get_details(self, url):
        '''Method to extract Postal Code from Immoweb using Selenium'''
        from selenium import webdriver

        # Initialize the WebDriver
        driver = webdriver.Chrome()

        # Navigate to the webpage
        driver.get(url)
        driver.implicitly_wait(20)
        # Execute JavaScript to access elements within the Shadow DOM
        element_inside_shadow_dom = driver.execute_script('return document.getElementById("usercentrics-root").shadowRoot.querySelector(\'button[data-testid="uc-accept-all-button"]\')')
        driver.implicitly_wait(20)
        # Now, you can interact with the element
        if element_inside_shadow_dom:
            # Perform actions on the element, for example, click on it
            element_inside_shadow_dom.click()
        else:
            print("Element inside Shadow DOM not found.")

        # Close the WebDriver
        driver.quit()


        
        
        #from selenium import webdriver

        # Execute JavaScript to find the Shadow DOM element and click on the button
        
        #driver = webdriver.Chrome() # Using Chrome because apparently Firefox has issues when it comes to shadow roots
        #wait = WebDriverWait(driver, 10) # Testing first way to solve error
        #driver.get(url)
        #shadow = Command().GET_SHADOW_ROOT
        #driver.execute_script('''
            #var shadowHost = document.getElementById("usercentrics-root");
            #var shadowRoot = shadowHost.shadowRoot;
            #var button = shadowRoot.querySelector("#uc-accept-all-button");
            #button.click();
        #''')
        #driver.implicitly_wait(10) # Testing secondway to solve error
        #wait.until(EC.presence_of_element_located((By.XPATH, "//div[@data-testid='uc-accept-all-button']")))
        #cookie_button =WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#uc-accept-all-button")))
        #shadow_host = driver.find_element(By.ID, "usercentrics-root")
        #shadow_root = shadow_host.shadow_root

       # cookie_button = shadow_root.find_element(By.CSS_SELECTOR, "#uc-accept-all-button") # <- Error occurs here
        #cookie_button = driver.find_element(By.XPATH, "//div[@data-testid='uc-accept-all-button']")
        #cookie_button.click()
        #driver.quit()



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
        
                
  