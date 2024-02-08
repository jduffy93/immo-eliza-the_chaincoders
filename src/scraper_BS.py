#imports

import concurrent.futures
import re
import threading
import time

import requests
from bs4 import BeautifulSoup as bs

thread_local = threading.local()
class Scraper():
    '''Docstring here'''

    def __init__(self, root_url, pages:int=1000) -> None:
        self.root_url = root_url
        self.pages = pages

    def scrape(self):
        """Scrape the website for listings."""
        list_of_details = self._get_all_listings_details()
        return list_of_details
    
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
            property_details["Postcode"] = "N/A"
            print("Postcode not found")
        #print("found details for: ", property_details["Property_ID"])
        return property_details
    
    def _get_all_listings_details(self):
        """Get the details of all the listings."""
        urls = self._get_listings_urls()
        list_of_details = []
       
        with concurrent.futures.ThreadPoolExecutor(max_workers=60) as executor:
           for result in  executor.map(self._get_listing_details, urls):
                if result:
                    list_of_details.append(result)
        return list_of_details
        
    def _get_listings_urls(self):
        """Scrape the website for listings."""
        list_of_urls = []
        start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=60) as executor:
            for result in executor.map(self._get_page_url, range(1, self.pages+1)):
                if result:
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
        

    #def remove_duplicates(self, filepath):
        pass


    #def clean_data(self, filepath):
        pass

    #def remove_empty_rows(self, filepath):
        pass


    #def to_csv(self, filepath):
      #with open('../csv_files/houses_apartments_urls.csv', 'w') as file:
          #for page_url in houses_url:
              #pass
          #for url in page_url:
              #file.write(url+'\n')

