#imports

import concurrent.futures
import re
import threading
import time

import requests
from bs4 import BeautifulSoup as bs

import re

import json
import pandas as pd
import numpy as np
#from IPython.display import display

thread_local = threading.local()

class Scraper():
    '''Docstring here'''

    def __init__(self):
        self.root_url = "https://www.immoweb.be/en/search/house/for-sale?countries=BE"
        self.pages = 10
        self.list_of_details = []

    
    def _get_all_listings_details(self):
        """Get the details of all the listings."""
        urls = self._get_listings_urls()
       
        with concurrent.futures.ThreadPoolExecutor(max_workers=60) as executor:
           for result in  executor.map(self._get_listing_details, urls):
                if result:
                    self.list_of_details.append(result)

    
    def _get_session(self):
        """Get a session for the current thread."""
        if not hasattr(thread_local, "session"):
            thread_local.session = requests.Session()
        return thread_local.session

    
    def _get_listing_details(self,url:str):
        """Get the details of a listing from a given URL."""
        session = self._get_session()
        req = session.get(url)
        
        if req.status_code != 200:
            print(f"{req.status_code}: Website could not be reached!")
            return
            
        soup = bs(req.content,'html.parser')
        property_details = {}

        
        #Immoweb ID:
        for elem_id in soup.find_all("div", attrs={"class": "classified__header--immoweb-code"}):
            property_details["Property_ID"] = re.sub(r'\D', '', elem_id.text.strip())  # Extract only digits
        
        #Locality:
        property_details["Locality"] = (url.split('/')[-3]).capitalize()
        
        #Postal code check this!:
        property_details["Postal_code"] = re.search(r'/(?P<postcode>\d{4})/',url).group('postcode')          
        
        #Price:
        for elem_price in soup.find_all("p", attrs = {"class":"classified__price"}):
            property_details["Price"] = elem_price.text.split()
            
        #Subtype of property:
        property_details["Subtype_of_property"] = (url.split('/')[-5]).capitalize()
        
        #Type of property:
        if property_details["Subtype_of_property"] == "House" or property_details["Subtype_of_property"] == "Apartment":
            property_details["Type_of_property"] = property_details["Subtype_of_property"]
        else:
            property_details["Type_of_property"] = "House"
            
        #Type of sale

        #table details:
        for row in soup.find_all("tr", attrs = {"class":"classified-table__row"}):
            key_element = row.find("th")
            if key_element:
                key = key_element.contents[0].strip()
                value_element = row.find("td")
                if value_element:
                    value = value_element.contents[0].strip()
                    property_details[key] = value

        for elem in soup.find_all("div", attrs={"class": "classified__header--immoweb-code"}):
            property_details["Property_ID"] = re.sub(r'\D', '', elem.text.strip())  # Extract only digits
        postcode_search = re.search(r'/(?P<postcode>\d{4})/',url)
        
        if postcode_search:
            property_details["Postcode"] = postcode_search.group('postcode')
        else:
            property_details["Postcode"] = None
            print("Postcode not found")
            

        #print("found details for: ", property_details["Property_ID"])
        return property_details
    

        
    def _get_listings_urls(self):
        """Scrape the website for listings."""
        list_of_urls = []
        
        start_time = time.time()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=60) as executor:
            for result in executor.map(self._get_page_url, range(1, self.pages+1)):
                if result: #!= None:
                    list_of_urls.extend(result)

        duration = time.time() - start_time
        
        print(f"found total of {len(list_of_urls)} urls in {duration} seconds")
        return list_of_urls
        #saving list of urls to a file, so as not torun until concurrency is implemented

    def _get_page_url(self, page:int):
        """Get the URL of a specific page."""
        url = f"{self.root_url}&page={page}"
        #print(url)
        page_req = requests.Session().get(url)
        
        if page_req.status_code != 200:
            print(f"{page_req.status_code}: Website could not be reached!")
            return None
        else:
            list_of_urls = []
            page_soup = bs(page_req.content, "html.parser")
            for listing in page_soup.find_all("a", attrs = {"class":"card__title-link"}):
                listing = listing.get("href")
                list_of_urls.append(listing)
                
        print(page)
        print("total number of urls on page: ", len(list_of_urls))
        return list_of_urls

        

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

