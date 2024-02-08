# Property Price Scraper

## Description
The Immoweb scraper is a Python program designed to extract information about properties for sale from the Immoweb website. It retrieves data from the website, organizes it into dictionaries, cleans the data, transforms it into a structured format, and saves it into a CSV file for further analysis.

## Features
* Scrapes Immoweb website for sale properties
* Creates a dictionary for each listing and its details
* Organizes all listings' details into a dictionary
* Cleans the data by removing duplicates, null values, and empty lines
* Transforms the data into a pandas DataFrame
* Saves the data into a CSV file for easy access and analysis

## Dependencies

* Python 3.12.1
* requests 2.31.0
* beautifulsoup4 4.12.3
* pandas 2.2.0

## Installation

1. Clone this repository to your local machine:

```cmd
git clone https://github.com/jduffy93/immo-eliza-scraping-the_chaincoders.git
```
2. Go to the **immo-eliza-scraping-the-chaincoders** directory:

```cmd
cd directory/immo-eliza-scraping-the-chaincoders
```

3. Install the required packages:

```cmd
pip install -r requirements.txt
```

## Running immo-eliza-scraping-the-chaincoders

You can use the program by running ``` python main.py ```

## Output

The output will be a data.csv file that is saved in the working folder in your computer. 

## Roadmap

Further improvements would include finding a solution to extract the "Type of sale" feature from the Immoweb website (New buildings and annuity sales, etc..). \
Implementing a dynamic range of the pages scraped (instead of having a fixed limit of 1000). \
Automating the binary column conversion. \
Increasing the pool of website that the program is able to scrape. \

## Outlook

The dataset will later be used to create a prediction model of the property prices in Belgium. 

