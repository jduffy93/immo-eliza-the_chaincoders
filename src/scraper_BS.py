#imports
#from selenium import webdriver
#from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup as bs
import re

import json
import pandas as pd
import numpy as np
from IPython.display import display

class Scraper():
    '''Docstring here'''

    def __init__(self):
        self.list_of_urls = []
        self.list_of_details = []
        
    def check_status(self, url: str):
        self.url = url
        self.req = requests.Session().get(self.url)

        if self.req.status_code != 200:
            print(f"{self.req.status_code}: Website could not be reached!")
        '''    
        #accessing the url with Selenium:
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(options=options)
        
        driver.get(url)
        self.page_source = driver.page_source
        driver.quit()
        '''
    def listing_listings(self):
        root_url = "https://www.immoweb.be/en/search/house/for-sale?countries=BE"
        #html = requests.Session().get(root_url)
        #soup = bs(html.content,'html.parser')
        #listings = []
        
        #for i in soup.find_all("a", attrs= {"class":"pagination__link button button--text button--size-small"}):
            #print(i)
        #total_items = pagination_list.find("span", attrs = {"class": "sr-only"})
        #total_pages = int(total_items[-2].text.strip())
        #print("Total pages:", total_pages)

        for i in range(2): #to be changed to the total_pages var:
            url = f"{root_url}&page={i}"
            #print(url)
            page_req = requests.Session().get(url)
            page_soup = bs(page_req.content, "html.parser")
            for listing in page_soup.find_all("a", attrs = {"class":"card__title-link"}):
                listing = listing.get("href")
                self.list_of_urls.append(listing)
        print(len(self.list_of_urls))

    
    def listing_details(self):
        soup = bs(self.req.content,'html.parser')
        property_details = {}  
        #selenium_soup = bs(self.page_source, features="html.parser")
        #print(selenium_soup.prettify())
        
        #Immoweb ID:
        for elem_id in soup.find_all("div", attrs={"class": "classified__header--immoweb-code"}):
            property_details["Property_ID"] = re.sub(r'\D', '', elem_id.text.strip())  # Extract only digits
        
        #Locality:
        property_details["Locality"] = (self.url.split('/')[-3]).capitalize()
        
        #Postal code:
        property_details["Postcode"] = re.search(r'/(?P<postcode>\d{4})/',self.url).group('postcode')          
        
        #Price:
        for elem_price in soup.find_all("p", attrs = {"class":"classified__price"}):
            property_details["Price"] = re.sub(r'\D', '', elem_price.text.split())
            
        #Subtype of property:
        property_details["Subtype_of_property"] = (self.url.split('/')[-5]).capitalize()
        
        #Type of property:
        if property_details["Subtype_of_property"] == "House" or property_details["Subtype_of_property"] == "Apartment":
            property_details["Type_of_property"] = property_details["Subtype_of_property"]
        else:
            property_details["Type_of_property"] = "House"
            
        #Type of sale:
        for elem_new in selenium_soup.find_all('span', class_='flag-list__text'):
            property_details["Type_of_sale"] = elem_new[0].text

        #table details:
        for row in soup.find_all("tr", attrs = {"class":"classified-table__row"}):
            key_element = row.find("th")
            if key_element:
                key = key_element.contents[0].strip()
                value_element = row.find("td")
                if value_element:
                    value = value_element.contents[0].strip()
                    property_details[key] = value

        return property_details 
        
        #self.list_of_details.append(property_details)
        

    def remove_duplicates(self, filepath):
        pass


    def clean_data(self):
        self.df = pd.DataFrame([listing for listing in self.list_of_details],dtype=object).fillna(np.nan).replace([np.nan], [None])
        
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)

        #print(self.df)
        binary_columns = ['Dining room',
                          'Office',
                          'Furnished',
                          'Gas, water & electricity',
                          'Double glazing',
                          'Subdivision permit',
                          'Possible priority purchase right',
                          'Proceedings for breach of planning regulations',
                          'Tenement building',
                          'Basement',
                          'Terrace',
                          'Attic',
                          'Thermic solar panels',
                          'Laundry room',
                          'Flat land',
                          'Garden',
                          'Conformity certification for fuel tanks',
                          'Planning permission obtained']
        
        self.df['Planning permission obtained'] = (self.df['Planning permission obtained'] == 'Yes').astype(int)
        
        print(self.df)
        #print(self.df[['Planning permission obtained']])
        
        print(self.df.columns)

    def remove_empty_rows(self, filepath):
        pass


    #def to_csv(self, filepath):
      #with open('../csv_files/houses_apartments_urls.csv', 'w') as file:
          #for page_url in houses_url:
              #pass
          #for url in page_url:
              #file.write(url+'\n')

