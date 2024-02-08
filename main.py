#from src.Skeleton_Code import Scraper
from src.scraper_BS import Scraper


if __name__ == "__main__":
    
    list_of_urls = [
        "https://www.immoweb.be/en/classified/apartment-block/for-sale/forest/1190/11120343",
        "https://www.immoweb.be/en/classified/house/for-sale/faimes/4317/11109944",
        "https://www.immoweb.be/en/classified/villa/for-sale/woluwe-saint-lambert/1200/11118328",
        "https://www.immoweb.be/en/classified/bungalow/for-sale/waterloo/1410/11122971",
        "https://www.immoweb.be/en/classified/house/for-sale/antwerpen-deurne/2100/11108152" ]

    scraper = Scraper()

    for url in list_of_urls:
        scraper.check_status(url)

        #print(url)
        scraper.listing_details() # Beautifulsoup
        print(scraper.listing_details())
    #print(scraper.list_of_details)
