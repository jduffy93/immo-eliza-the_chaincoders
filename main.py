#from src.Skeleton_Code import Scraper
from src.scraper_BS import Scraper

if __name__ == "__main__":

    scraper = Scraper()
    list_of_details = scraper._get_all_listings_details()

    #print(scraper.list_of_details)
    print(len(scraper.list_of_details))
    #scraper = Scraper()
    #for url in scraper.list_of_urls:
        #scraper.check_status(url)

        #print(url)
        #scraper.listing_details() # Beautifulsoup

    # print(scraper.list_of_details)
    
    scraper.clean_data()


    
    #print(scraper.list_of_details)

