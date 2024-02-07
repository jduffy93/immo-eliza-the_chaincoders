#imports

import requests
from bs4 import BeautifulSoup as bs
import re
import json

class Scraper():
    '''Docstring here'''

    def __init__(self):
        self.list_of_details = []
        

    def check_status(self, url: str):
        self.url = url
        self.req = requests.Session().get(self.url)

        if self.req.status_code != 200:
            print(f"{self.req.status_code}: Website could not be reached!")
            
    def listing_listings(root_url):
        pass 
    
    def listing_details(self):
        soup = bs(self.req.content,'html.parser')
        property_details = {}  
        
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

        property_details["Postcode"] = re.search(r'/(?P<postcode>\d{4})/',self.url).group('postcode')
        
        self.list_of_details.append(property_details)
        

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