#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pathlib

import geodatasets

# geopandas map of the USA
import geopandas
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim

# In[2]:


collaborators_file_path = pathlib.Path("../data/Way_Lab_Collaborators.csv")
df = pd.read_csv(collaborators_file_path)
df.head()


# In[3]:


# get the latitude and longitude of each city, state, country combination
# using the geopy library

geolocator = Nominatim(user_agent="http")

# initialize the location column
df["location"] = df["City"] + ", " + df["State"] + ", " + df["Country"]
df["latitude"] = np.nan
df["longitude"] = np.nan

for i in range(len(df)):
    try:
        location = geolocator.geocode(df["location"][i], timeout=100)
        df.loc[i, "latitude"] = location.latitude
        df.loc[i, "longitude"] = location.longitude
    except:
        print(f"Error: {df['location'][i]} not found")


# In[4]:


gdf = geopandas.GeoDataFrame(
    df, geometry=geopandas.points_from_xy(df.longitude, df.latitude), crs="EPSG:4326"
)
gdf.head()


# In[5]:


# save the geopandas dataframe to a shapefile
gdf.to_file("../data/collaborator_locations.shp")
