#from src.Skeleton_Code import Scraper
from src.scraper_BS import Scraper

if __name__ == "__main__":
    
    ROOT_URL = "https://www.immoweb.be/en/search/house/for-sale?countries=BE"
    scraper = Scraper(ROOT_URL,333)

    list_of_details = scraper.scrape()

    print(list_of_details)

    #for url in scraper.list_of_urls:
        #scraper.check_status(url)

        #print(url)
        #scraper.listing_details() # Beautifulsoup

    # print(scraper.list_of_details)
