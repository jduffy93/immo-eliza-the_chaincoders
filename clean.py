import pandas as pd
import numpy as np

'''This script further cleans the 'details_clean_initial.csv' in preperation for the ML Model.'''


immo = pd.read_csv('data/clean/details_clean_initial.csv')
immo = immo.replace(np.nan, None)

# Replace 'Not specified' with None as in this case it serves no purpose. If a consumption is not provided it might as well be absent
immo['Primary energy consumption'] = immo['Primary energy consumption'].replace('Not specified', None)
immo['CO₂ emission'] = immo['CO₂ emission'].replace('Not specified', None)
immo['Yearly theoretical total energy consumption'] = immo['Yearly theoretical total energy consumption'].replace('Not specified', None)

# Remove annuity properties
substring = '€'
filter = immo['Price'].str.contains(substring)
immo = immo[~filter]

# Remove group developments for dataset
immo = immo[
    (immo["Subtype_of_property"] != "New-real-estate-project-houses")
    & (immo["Subtype_of_property"] != "New-real-estate-project-apartments")
]

# Remove substrings from strings
immo['Price'] = immo['Price'].str.replace(r'Starting price : ','')
immo['CO₂ emission'] = immo['CO₂ emission'].str.replace(r' kg CO₂/m²','')
immo['Yearly theoretical total energy consumption'] = immo['Yearly theoretical total energy consumption'].str.replace(r' kWh/year','')
immo['Building price excluding VAT'] = immo['Building price excluding VAT'].str.replace(r'€','')
immo['Building price excluding VAT'] = immo['Building price excluding VAT'].str.replace(r',','')
immo['Total price including taxes*'] = immo['Total price including taxes*'].str.replace(r'€','')
immo['Total price including taxes*'] = immo['Total price including taxes*'].str.replace(r',','')
immo['Street frontage width'] = immo['Street frontage width'].str.replace(r' m','')

# Remove 'Unnamed: 0' column as that seems to just be a key column generated from 'raw' data
immo.drop(columns='Unnamed: 0', inplace=True)
immo.drop(columns='Maximum duration of annuity', inplace=True)            


# Lists to map columns to correct type
map_to_float = [
    "Price",
    "Number of floors",
    "Number of frontages",
    "Covered parking spaces",
    "Outdoor parking spaces",
    "Living area",
    "Bedrooms",
    "Bedroom 1 surface",
    "Bedroom 2 surface",
    "Bedroom 3 surface",
    "Bedroom 4 surface",
    "Bedroom 5 surface",
    "Bathrooms",
    "Toilets",
    "Surface of the plot",
    "Width of the lot on the street",
    "Garden surface",
    "Terrace surface",
    "CO₂ emission",
    "Yearly theoretical total energy consumption",
    "Total ground floor buildable",
    "Cadastral income",
    "Shower rooms",
    "Living room surface",
    "Kitchen surface",
    "Office surface",
    "Basement surface",
    "Attic surface",
    "E-level (overall energy performance)",
    "How many fireplaces?",
    "Floor",
    "Professional space surface",
    "Number of annexes",
    "Building price excluding VAT",
    "Number of annuitants",
    "Age of annuitant",
    "Percentage rented",
    "Current monthly revenue",
    "Construction year",
    "Postcode",
    "Street frontage width",
    "Monthly charges",
    "Primary energy consumption"
]


immo[map_to_float] = immo[map_to_float].astype(float).round(2)

# We create a new column called 'Municipality', which is based on the postcode
# Brussels: numbers from 1000 to 1100
# Flanders: numbers from 1500 to 4000 and 8000 to 10000
# Wallonia: numbers from 1100 to 1500 and from 4000 to 8000


brussels_range = range(1000,1100)
flanders_range = list(range(1500,4000)) + list(range(8000,10000))
wallonia_range = list(range(1100,1500)) + list(range(4000,8000))

def municipality_from_pc(postcode):
    if postcode in brussels_range:
        return "Brussels"
    elif postcode in flanders_range:
        return "Flanders"
    elif postcode in wallonia_range:
        return "Wallonia"
    
immo["Municipality"] = immo["Postcode"].apply(municipality_from_pc)


# Here we will remove empty columns
immo.dropna(how='all', axis=1, inplace=True)

# Here we will drop rows with a certain percentage of missing data (>=95%)
missing_proportion = immo.isnull().mean()
names = missing_proportion[missing_proportion > 0.95].index
immo.drop(columns=names, inplace=True)
immo.drop(columns='Building price excluding VAT', inplace=True) # Has the same values as Price, but more missing values


# Here we will remove the outliers in price
# Calculate interquartile range and outliers
Q1 = immo['Price'].quantile(0.25)
Q3 = immo['Price'].quantile(0.75)
IQR = Q3 - Q1

# Calculate the upper whisker
upper_whisker = immo['Price'][immo['Price'] <= Q3 + 1.5 * IQR].max()

immo = immo[immo["Price"] < upper_whisker]


immo.to_csv('data/clean/details_clean_final.csv') # Save cleaned data