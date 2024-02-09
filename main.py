from src.scraper_BS import ImmowebScraper

if __name__ == "__main__":

    scraper = ImmowebScraper()

    list_of_details = scraper.get_all_listings_details()
    scraper.clean_data()
    scraper.write_terminal()


