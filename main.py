from src.scraper_BS import Scraper

if __name__ == "__main__":

    scraper = Scraper()
    list_of_details = scraper._get_all_listings_details()

    print(scraper.list_of_details)
    print(len(scraper.list_of_details))
    
    scraper.clean_data()


