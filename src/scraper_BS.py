import concurrent.futures
import re
import threading

import requests
from bs4 import BeautifulSoup as bs

import pandas as pd
import numpy as np


thread_local = threading.local()

class Scraper():
    '''Docstring here'''

    def __init__(self):
        self.root_url = "https://www.immoweb.be/en/search/house/for-sale?countries=BE"
        self.pages = 332
        self.terminal_outputs = []
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

    
    def _get_listing_details(self, url: str) -> None:
        """Get the details of a listing from a given URL."""
        session = self._get_session()
        req = session.get(url)
        
        if req.status_code != 200:
            print(f"{req.status_code}: Website could not be reached! Here is the Url: {url}")
            self.terminal_outputs.append(f"{req.status_code}: Website could not be reached! Here is the Url: {url}\n")
            return
            
        soup = bs(req.content,'html.parser')
        property_details = {}

        # Immoweb ID:
        for elem_id in soup.find_all("div", attrs={"class": "classified__header--immoweb-code"}):
            property_details["Property_ID"] = re.sub(r'\D', '', elem_id.text.strip())  # Extract only digits
        
        # Locality:
        property_details["Locality"] = (url.split('/')[-3]).capitalize()
        
        # Price:
        for elem_price in soup.find_all("p", attrs = {"class":"classified__price"}):
            property_details["Price"] = elem_price.text.split()
            
        # Subtype of property:
        property_details["Subtype_of_property"] = (url.split('/')[-5]).capitalize()
        
        # Type of property:
        if property_details["Subtype_of_property"] == "House" or property_details["Subtype_of_property"] == "Apartment":
            property_details["Type_of_property"] = property_details["Subtype_of_property"]
        else:
            property_details["Type_of_property"] = "House"
            
        # Table details:
        # Iterate over each row in the table of property details 
        for row in soup.find_all("tr", attrs = {"class":"classified-table__row"}):
            key_element = row.find("th") # Find the key element (the table header)

            if key_element: 
                key = key_element.contents[0].strip() # Extract the key text and strip any leading/trailing whitespace
                value_element = row.find("td") # Find the value element (the table data)

                if value_element:
                    value = value_element.contents[0].strip() # Extract the value text and strip any leading/trailing whitespace
                    property_details[key] = value # Add the key-value pair to the property details dictionary

        # Extract the property ID from the page
        for elem in soup.find_all("div", attrs={"class": "classified__header--immoweb-code"}):
            property_details["Property_ID"] = re.sub(r'\D', '', elem.text.strip())  # Extract only digits
        
        # Extract the postcode from the URL
        postcode_search = re.search(r'/(?P<postcode>\d{4})/',url)
        if postcode_search:
            property_details["Postcode"] = postcode_search.group('postcode')
        else:
            property_details["Postcode"] = None

        # Add url to the dictionary
        property_details["Url"] = url

        return property_details
    

    def _get_listings_urls(self):
        """Scrape the website for listings."""
        list_of_urls = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=60) as executor:
            for result in executor.map(self._get_page_url, range(1, self.pages+1)):
                if result: #!= None:
                    list_of_urls.extend(result)

        return list_of_urls


    def _get_page_url(self, page:int):
        """Get the URL of a specific page."""
        url = f"{self.root_url}&page={page}"

        page_req = requests.Session().get(url)
        
        if page_req.status_code != 200:
            print(f"{page_req.status_code}: Website could not be reached! Here is the url: {url}")
            self.terminal_outputs.append(f"{page_req.status_code}: Website could not be reached! Here is the url: {url}\n")
            return None
        else:
            list_of_urls = []
            page_soup = bs(page_req.content, "html.parser")

            # Extract the URLs of the listings on the page
            for listing in page_soup.find_all("a", attrs = {"class":"card__title-link"}):
                listing = listing.get("href")
                list_of_urls.append(listing)
                
        return list_of_urls


    def clean_data(self):
        """
        Clean the scraped data and convert it into a DataFrame.

        This method takes the list of property details, converts it into a DataFrame, 
        and cleans the data by replacing missing values with None. It also converts 
        the binary_columns list to binary format (1 for 'Yes', 0 for 'No').
        """

        # Convert the list of property details into a DataFrame
        # Replace missing values with None
        self.df = pd.DataFrame([listing for listing in self.list_of_details],dtype=object).fillna(np.nan).replace([np.nan], [None])
        
        self.df.to_csv('data/details_raw.csv') # Save raw data

        # List of column names that have binary (Yes, No) values
        binary_columns = ['Dining room',
                          'Office',
                          'Furnished',
                          'Gas, water & electricity',
                          'Double glazing',
                          'Subdivision permit',
                          'Possible priority purchase right',
                          'Tenement building',  
                          'Basement',
                          'Terrace',
                          'Attic',
                          'Thermic solar panels',
                          'Laundry room',
                          'Flat land',
                          'Garden',
                          'Conformity certification for fuel tanks',
                          'Planning permission obtained'
                          ] # Would be better if this could be automatically generated instead of manually  specified
        
        self.df[binary_columns] = (self.df[binary_columns] == 'Yes').astype(int) # Convert Yes/No to 1/0

        # Append various bits of info to be saved to a txt file later on
        self.terminal_outputs.append(f"Size of the dataframe: {self.df.shape} \n")
        self.terminal_outputs.append(f"Total number of properties (houses, apartments, ...): {self.df.shape[0]} \n")
        self.terminal_outputs.append(f"Total number of features per property: {self.df.shape[1]} \n")

        self.terminal_outputs.append(f"List of column names: \n{self.df.columns.tolist()}\n")

        self.df.to_csv('data/details_clean.csv') # Save 'clean' data


    #### CHECK TERMINAL OUTPUT FOR ALL ERROR CODES
    def write_terminal(self):
        """Save terminal output to a text file"""

        with open("src/terminal_output.txt", "w", encoding="utf-8") as output:
            for line in self.terminal_outputs:
                output.write(line)



