from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import pandas as pd


df = pd.read_excel('Data/disabilitycensus2021.xlsx', sheet_name='Table 6')


import pandas as pd
# Example list of boroughs
boroughs = df['Local Authority'].unique()

# Initialize Nominatim API
geolocator = Nominatim(user_agent="uk_boroughs_geocoder")

# Use rate limiter to avoid hitting API limits
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

# Fetch latitude and longitude for each borough
locations = [geocode(f"{borough}, UK") for borough in boroughs]

# Extracting latitude and longitude
lat_lon = [(location.latitude, location.longitude) if location else (None, None) for location in locations]

# Creating a DataFrame
df = pd.DataFrame(lat_lon, columns=['Latitude', 'Longitude'], index=boroughs)

print(df)


df.to_excel('Data/boroughs_lat_lon.xlsx')

