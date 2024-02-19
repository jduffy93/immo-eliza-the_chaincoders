# Property Price Scraper


## Description
The Immoweb scraper is a Python program designed to extract information about properties for sale from the Immoweb website and is divided into four phases where phase three and four will be described later on in our separate repositories. It retrieves data from the website, organizes it into dictionaries, cleans the data, transforms it into a structured format, and saves it into a CSV file for further analysis.

Phase 1 Data Clean the dataset so that it does not contain any duplicates, blank spaces or errors. 

Phase 2 Exploratory Data Analysis where vizualization is explored, ephasizing on the Structure of the data (rows and columns), correlation between the variables to each other and to price, and explore Which variables have the greatest and least influence on the price.


## Features
* Scrapes Immoweb website for sale properties
* Extracts the details for each listing
* Cleans the data by removing duplicates and empty lines
* Saves the data to CSV files 


## Dependencies

* Python 3.12.1
* requests 2.31.0
* beautifulsoup4 4.12.3
* pandas 2.2.0
* numpy
* seaborn
* matplotlib


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

Make sure you are in the correct directory (/immo-eliza-scraping-the-chaincoders), if not go to the directory:

 ```cmd
 cd directory/immo-eliza-scraping-the-chaincoders
 ```

Run immo-eliza-scraping-the-chaincoders from main:

```cmd
python main.py
```


## Output

The ouptuts for the data are saved in the ```data/``` folder as CSV files. Extra information with certain errors are saved in ```src/terminal_output.txt```.

Output preview:

![Scraper-output](./assets/output_snippet.png)


## Outlook

The dataset will later be used to create a predictive model of the property prices in Belgium.

