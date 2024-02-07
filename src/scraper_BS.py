#imports

import requests
from bs4 import BeautifulSoup as bs
import re
import json

class Scraper():
    def __init__(self, url:str):
        self.url = url
        self.req = requests.Session().get(url)
        
        if self.req.status_code != 200:
            print(f"{self.req.status_code}: Website could not be reached!")
            
    def listing_listings(self):
        root_url = "https://www.immoweb.be/en/search/house/for-sale?countries=BE"
        html = requests.Session().get(root_url)
        soup = bs(html.content,'html.parser')
        listings = []
        
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
                listings.append(listing)
        print(len(listings))
        return listings
    
    def listing_details(self):
        soup = bs(self.req.content,'html.parser')
        #print(soup)
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
            
        for elem2 in soup.find_all():
            pass

        property_details["Postcode"] = re.search(r'/(?P<postcode>\d{4})/',self.url).group('postcode')
        
        #for elem2 in soup.find_all("div", attrs={"class":"classified__information--address"}):
            #property_details["Postal_Code"] = #re.sub(r'\D', '', elem2.text.strip())
    
        return property_details 
        
#TEST        
house = Scraper("https://www.immoweb.be/en/classified/apartment-block/for-sale/forest/1190/11120343")
#print(house.listing_details())
        
print(house.listing_listings())
