import folium
import pandas

"Take data from external file and separate columns"
data = pandas.read_csv("Volcanoes_USA.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])

def colour_selector(elevation):
    if elevation < 1000:
        return "green"
    elif 1000 <= elevation < 3000:
        return "orange"
    else:
        return "red"

"Create Webmap and starting location"
map = folium.Map(location=[51.5, 0], zoom_start=4, tiles="Mapbox Bright")

"Create volcanoe feature group"
fgv = folium.FeatureGroup(name="Volcanoes")

for lt, ln, el in zip(lat, lon, elev):
    fgv.add_child(folium.CircleMarker(location=[lt, ln], radius=5, color=colour_selector(el), fill=True, popup=str(el)))

"Create population feature group"
fgp = folium.FeatureGroup(name="Population")

fgp.add_child(folium.GeoJson(data=open("world.json", "r", encoding="utf-8-sig").read(),
style_function=lambda x: {"fillColor":"green" if x["properties"]["POP2005"] < 10000000
else "yellow" if 10000000 <= x["properties"]["POP2005"] < 20000000 else "red"}))

"Attach feature groups to Webmap"
map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())

map.save("Map1.html")
