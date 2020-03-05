# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 13:20:54 2019

@author: Sayantan
"""

import folium
import pandas

data = pandas.read_csv("lat_lon_data.csv")
lat = list(data["latitude"])
lon = list(data["longitude"])
title = list(data["title"])
city = list(data["city"])
state = list(data["state"])

def color_define(state_color):
    if "M" in state_color:
        return "green"
    elif "A" in state_color:
        return "blue"
    else:
        return "red"
        

html = """<h4>Information:</h4>
Title: %s<br>
City: %s<br>
State: %s<br>
"""

webmap = folium.Map(location=[40,-70],zoom_start=6,tiles="Stamen Terrain")
fgv = folium.FeatureGroup(name="Airports")

for lt, ln, ct, tl, st in zip(lat, lon, city, title, state):
    iframe= folium.IFrame(html=html %(tl,ct,st),width=200,height=100)
    fgv.add_child(folium.CircleMarker(location=[lt,ln],popup=folium.Popup(iframe),radius=7,color='grey',fill_color=color_define(st),fill_opacity=0.6))

fgp = folium.FeatureGroup(name="Population")    
fgp.add_child(folium.GeoJson(data=open('world.json','r',encoding='utf-8-sig').read(),
style_function=lambda x:{'fillcolor':'green' if x['properties']['POP2005'] < 1000000
else 'orange' if 1000000<= x['properties']['POP2005'] < 2000000 else 'red'}))

webmap.add_child(fgp)
webmap.add_child(fgv)
webmap.add_child(folium.LayerControl())
webmap.save("WebMap.html")