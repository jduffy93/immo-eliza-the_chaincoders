import pandas as pd
import numpy as np



# Not completed





immo = pd.read_csv('data/clean/details_clean.csv')
print('1', type(immo))
immo = immo.replace(np.nan, None)
print('2', type(immo))

# Replace 'Not specified' with None as in this case it serves no purpose. If a consumption is not provided it might as well be absent
immo['Primary energy consumption'] = immo['Primary energy consumption'].replace('Not specified', None)
immo['CO₂ emission'] = immo['CO₂ emission'].replace('Not specified', None)
#immo['Yearly theoretical total energy consumption'] = immo['Yearly theoretical total energy consumption'].str.strip()
#immo['Yearly theoretical total energy consumption'] = immo['Yearly theoretical total energy consumption'].replace('Not specified', None)
print('3', type(immo))

# Remove annuity properties
substring = '€'
filter = immo['Price'].str.contains(substring)
immo = immo[~filter]

print('4', type(immo))

# Remove group developments for dataset
immo = immo[
    (immo["Subtype_of_property"] != "New-real-estate-project-houses")
    & (immo["Subtype_of_property"] != "New-real-estate-project-apartments")
]
print('5', type(immo))


# Remove substrings from strings
immo['Price'] = immo['Price'].str.replace(r'Starting price : ','')
immo['CO₂ emission'] = immo['CO₂ emission'].str.replace(r' kg CO₂/m²','')
#immo['Yearly theoretical total energy consumption'] = immo['Yearly theoretical total energy consumption'].str.replace(r' kWh/year','')
immo['Building price excluding VAT'] = immo['Building price excluding VAT'].str.replace(r'€','')
immo['Building price excluding VAT'] = immo['Building price excluding VAT'].str.replace(r',','')
immo['Total price including taxes*'] = immo['Total price including taxes*'].str.replace(r'€','')
immo['Total price including taxes*'] = immo['Total price including taxes*'].str.replace(r',','')
immo['Street frontage width'] = immo['Street frontage width'].str.replace(r' m','')
print('6', type(immo))
print()

# Remove 'Unnamed: 0' column as that seems to just be a key column generated from 'raw' data
immo = immo.drop(columns='Unnamed: 0', inplace=True)
immo = immo.drop(columns='Yearly theoretical total energy consumption')
immo = immo.drop(columns='Maximum duration of annuity')            
    
print('7', type(immo))


immo.to_csv('data/clean/details_clean_2.csv') # Save clean data