import pandas as pd
import numpy as np

# Not completed

class Clean():
    """"""

    def __init__(self):
     pass


    def clean(self):

        immo = pd.read_csv('../data/clean/details_clean.csv')

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
            
            
            
            