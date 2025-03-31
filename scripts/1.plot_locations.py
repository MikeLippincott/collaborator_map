#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pathlib

# geopandas map of the USA
import geopandas
import matplotlib.pyplot as plt
import numpy as np

# plot on plotly map
import plotly.express as px

# In[2]:


# load in the map
world = geopandas.read_file("../data/110m_cultural.zip")
# read in the data from a shapefile
gdf = geopandas.read_file("../data/collaborator_locations.shp")
gdf.rename(
    columns={"Organizati": "Organization", "First coll": "First collaborated"},
    inplace=True,
)
# Add jitter to latitude and longitude
np.random.seed(0)
gdf["latitude_jittered"] = gdf["latitude"] + np.random.uniform(
    -0.001, 0.001, size=len(gdf)
)
gdf["longitude_jittered"] = gdf["longitude"] + np.random.uniform(
    -0.001, 0.001, size=len(gdf)
)

gdf.head()


# In[3]:


fig = px.scatter_map(
    gdf,
    lat="latitude_jittered",
    lon="longitude_jittered",
    hover_name="Name",
    hover_data=["Organization"],
    color="Projects",
    zoom=1,
    height=600,
    opacity=0.9,
    width=1100,
)

fig.update_layout(mapbox_style="carto-positron")
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
# change the size of the points
fig.update_traces(marker=dict(size=15))
fig.show()
# save the plot
pathlib.Path("../maps").mkdir(parents=True, exist_ok=True)
fig.write_html("../maps/collaborator_locations.html")


# In[ ]:
