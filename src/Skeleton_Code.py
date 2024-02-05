# to access the html content of a single property url
import requests 

# to select parts of an XML or HTML using BeautifulSoup
from bs4 import BeautifulSoup 

# to use regular expressions
import re 

# to build a dictionary form a string
import json 
 
class HouseApartmentScraping:
    
    def __init__(self, url):
        self.url = url
        
        self.html = requests.get(self.url).content
        self.soup = BeautifulSoup(self.html,'html.parser')
        
        self.house_dict = self.house_dict()
        
        self.property_ID = self.property_ID()
        self.locality = self.locality()
        self.postal_code = self.postal_code()
        self.price = self.price()
        self.type_property = self.type_property()
        self.subtype = self.subtype()
        self.type_sale = self.type_sale()
        self.num_rooms = self.num_rooms()
        self.living_area = self.living_area()
        self.equipped_kitchen = self.equipped_kitchen()
        self.furnished = self.furnished()
        self.open_fire = self.open_fire()
        self.terrace_area = self.terrace_area()
        self.garden_area = self.garden_area()
        self.surface_good = self.surface_good()
        self.num_facade = self.num_facade()
        self.pool = self.pool()
        self.state = self.state()

    # Store all houses urls in a csv file
    with open('../csv_files/houses_apartments_urls.csv', 'w') as file:
        for page_url in houses_url:
            pass
        for url in page_url:
            file.write(url+'\n')

    def remove_duplicates(self, filepath):
        pass

    def clean_data(self, filepath):
        pass

    def remove_empty_rows(self, filepath):
        pass

