from bs4 import BeautifulSoup as bs
import requests

class Scraper():
    def __init__(self, base_url:str):
        self.base_url = base_url

    def listing_listings(self):
        listings = []
        page = 1

        while True:
            url = f"{self.base_url}?countries=BE&page={page}"
            req = requests.get(url)
            if req.status_code != 200:
                print(f"{req.status_code}: Website could not be reached!")
                break

            soup = bs(req.content,'html.parser')

            # Check if a specific element that indicates the end of results is present
            # Replace 'css_selector' with the actual CSS selector
            if soup.select('css_selector'):
                break  # If the element is found, break the loop

            for listing in soup.find_all("a", attrs = {"class":"card__title-link"}):
                listing = listing.get("href")
                listings.append(listing)

            page += 1

        print(len(listings))
        return listings

# Create a Scraper for the listings
scraper = Scraper('https://www.immoweb.be/en/search/house/for-sale')

# Get the listings
listings = scraper.listing_listings()