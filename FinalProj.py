import pandas as pd
import streamlit as st
from PIL import Image

import math
from datetime import datetime

import pandas as pd

import folium
from streamlit_folium import folium_static

import requests
import json
import folium


#In this project you are going to use Airbnb NYC 2019 housing data to build a streamlit app with following requirements:
@st.cache_data
def data():
   url = "https://cis102.guihang.org/data/AB_NYC_2019.csv"
   return pd.read_csv(url)
data = data()
#1. [5pts] It greets users with a nice page with sufficient info describing the purpose of the webapp (you design your App name and logo etc.).
st.header('Airbnb 2019 NYC Snapshot') 
image = Image.open('airbnblogo.png')
st.image(image)
st.markdown('This interactive WebApp is a snapshot of Airbnb for the NYC region. It is based on AirBnb\'s housing data from 2019.')
#2.  [5pts] User will be able to see a few rows of the data as a table
st.markdown('Here\'s a short example of the database:')
st.dataframe(data.head(10))
#3.  [10pts] User will be able to select one of the five NYC boroughs (Manhattan, Bronx, etc. ) from a drop down menu - The candidate boroughs in menu must come from the dataset instead of hard coding it (bot like selection=["Manhattan", "Bronx", ...])
boroughs = list(set(data['neighbourhood_group']))
select_borough = st.selectbox("Select Borough:", boroughs, 0)
# 4.  [20pts] User will then be able to select one or more of the neighborhoods (if Manhattan is selected then this multi-select drop down menu will have neighborhoods available in Mahanttan)
InBorough = data['neighbourhood_group'] == str(select_borough)
ListHood = data[InBorough]
HoodInBorough = ListHood['neighbourhood']
sel_Hood = st.selectbox("Select Neighbourhood:", list(set(HoodInBorough)), 0)
#5.  [10pts] User should be able to set price range (on the main section instead of side menu)
PriceRange = st.slider("Price range", float(data.price.min()), 1000., (50., 300.))
#6.  [10pts] After all the previous selections user should see something like:
HousingInHood = data['neighbourhood'] == str(sel_Hood)
ListHousingInHood = data[HousingInHood]

PriceFilter = (ListHousingInHood['price'] >= PriceRange[0]) & (ListHousingInHood['price'] <= PriceRange[1])
CountedBudgetHousing = ListHousingInHood[PriceFilter]
st.write(f"Total {len(CountedBudgetHousing)} housing rental are found in {sel_Hood} {select_borough} with price between \${PriceRange[0]} and \${PriceRange[1]}")
#  Total 15 housing rental are found in Midtown Manhattan with price between $500 and $800
#the total entries can be 0
#7.  [20pts] At this step a map shows with available apartment/house as markers; when clicking on it it shows details including "name", host name, room type, neighborhood, Price will be showing as tool tip.
#e.g.,  Name: Furnished room in Astoria apartment
#       Neighborhood: Astoria
#       Host name: John
#       Room type: Private room
#       Tooltip: $1000

m = folium.Map(location=[CountedBudgetHousing['latitude'].iloc[0], CountedBudgetHousing['longitude'].iloc[0]], zoom_start=12)

for index, row in CountedBudgetHousing.iterrows():
    name = row['name']
    neighborhood = row['neighbourhood']
    host_name = row['host_name']
    room_type = row['room_type']
    price = row['price']
    tooltip = f"Name: {name}<br>Neighborhood: {neighborhood}<br>Host name: {host_name}<br>Room type: {room_type}<br>Price: ${price}"
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=tooltip
    ).add_to(m)
folium_static(m)

#8.  [10pts] Finally you should upload your app to streamlit site.
#Submit your webapp URL and share all your code and image files in a subfolder in your shared folder on google drive.