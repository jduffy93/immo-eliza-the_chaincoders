from src.scraper_BS import Scraper

if __name__ == "__main__":

    scraper = Scraper()

    list_of_details = scraper._get_all_listings_details()
    scraper.clean_data()
    scraper.write_terminal()


