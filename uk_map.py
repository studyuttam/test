import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import streamlit as st
import pandas as pd

# Example DataFrame
# Ensure your DataFrame has 'lat', 'lon', and 'population' columns for this to work
df = pd.DataFrame({
    'Local Authority': ['Example 1', 'Example 2'],
    'lat': [51.509865, 52.486243],
    'lon': [-0.118092, -1.890401],
    'population': [1000, 1500]
})

# Create a map centered around the UK
m = folium.Map(location=[55.3781, -3.4360], zoom_start=6)

# Add a bubble for each local authority
for index, row in df.iterrows():
    folium.Circle(
        location=[row['lat'], row['lon']],
        radius=row['population'] * 10,  # Adjust the multiplier for bubble size
        color='blue',
        fill=True,
        fill_color='blue',
        tooltip=f"{row['Local Authority']}: {row['population']}"
    ).add_to(m)

# Display the map in Streamlit
folium_static(m)