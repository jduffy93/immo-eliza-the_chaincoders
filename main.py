from src.Skeleton_Code import HouseApartmentScraping


if __name__ == "__main__":
    has = HouseApartmentScraping()
    
    #has.first_details('https://www.immoweb.be/en/classified/apartment-block/for-sale/forest/1190/11120343') # Beautifulsoup
    has.get_details('https://www.immoweb.be/en/classified/apartment-block/for-sale/forest/1190/11120343') # Selenium
