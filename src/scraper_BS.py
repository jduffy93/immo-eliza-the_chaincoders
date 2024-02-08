#imports

import requests
from bs4 import BeautifulSoup as bs
import re
import json

class Scraper():
    '''Docstring here'''

    def __init__(self):
        self.list_of_details = []
        self.list_of_urls = []   

    def check_status(self, url: str):
        self.url = url
        self.req = requests.Session().get(self.url)

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
        
        """
        page = 300  # Add a variable named "page" and assign it a value
        while True:
            url = f"{self.base_url}?countries=BE&page={page}"
            req = requests.get(url)

            soup = bs(req.content,'html.parser')

            # Check if a specific element that indicates the end of results is present
            # Replace 'css_selector' with the actual CSS selector
            if soup.select('css_selector'):
                break  # If the element is found, break the loop 
        """
        for i in range(1000): #to be changed to the total_pages var:
            url = f"{root_url}&page={i}"
            #print(url)
            page_req = requests.Session().get(url)
            if page_req.status_code != 200:
                print(f"{page_req.status_code}: Website could not be reached!")
                break
            else:
                page_soup = bs(page_req.content, "html.parser")
                for listing in page_soup.find_all("a", attrs = {"class":"card__title-link"}):
                    listing = listing.get("href")
                    self.list_of_urls.append(listing)
            print(i)        
        print(len(self.list_of_urls))
        #saving list of urls to a file, so as not torun until concurrency is implemented

        with open('urls.txt', 'w') as file:
            for line in self.list_of_urls:
                file.write(line)
                file.write('\n')    
        # return listings
    
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
            
        for elem2 in soup.find_all():
            pass

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

