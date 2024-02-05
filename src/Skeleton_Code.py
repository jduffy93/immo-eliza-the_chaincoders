# to access the html content of a single property url
from typing import Self
import requests 

# to select parts of an XML or HTML using BeautifulSoup
from bs4 import BeautifulSoup 

# to use regular expressions
import re 

# to build a dictionary form a string
import json 
 
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
        html = requests.get(url).content
        soup = BeautifulSoup(html,'html.parser')
       # for elem in soup.find_all("div", attrs = {"class":"classified__header--immoweb-code"}):
        #    self.property_info["Property_ID"] = elem
        for elem2 in soup.find_all("span", attrs = {"class":"classified__information--address-row"}):
            print(elem2)
       # print(self.property_info)
            
        #for elem in soup.find_all()   
        
                
                
example=HouseApartmentScraping()
example.first_details('https://www.immoweb.be/en/classified/apartment-block/for-sale/forest/1190/11120343')

                
            
        
            
            
        
        
        
        
        
   