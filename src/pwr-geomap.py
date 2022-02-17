# %%
from distutils.log import error
from multiprocessing.context import _default_context
import os
import pandas as pd
from geopy.geocoders import Nominatim
import folium
from branca.element import Figure

# %%
# Read in the data
file_dir = os.path.join(os.getcwd(), "../files/Untitled 18.csv")

df = pd.read_csv(file_dir)

# %%
# Test geo locater

geolocater = Nominatim(user_agent="tutorial")

location = geolocater.geocode("5491 Parkside Drive Brighton, MI 48114 ")

print(location.address)
print((location.latitude, location.longitude))

# %%
# Clean data
df = df.replace({r'\s+$': '', r'^\s+': ''}, regex=True).replace(r'\n',  ' ', regex=True).replace(r'\bDET\b', '', regex=True)

# %%
fig = Figure(width=550, height=400)
map = folium.Map(location=[42.3314, -83.0458], zoom_start=10)
fig.add_child(map)

folium.TileLayer('Stamen Terrain').add_to(map)
folium.TileLayer('Stamen Toner').add_to(map)
folium.TileLayer('Stamen Water Color').add_to(map)
folium.TileLayer('cartodbpositron').add_to(map)
folium.TileLayer('cartodbdark_matter').add_to(map)
folium.LayerControl().add_to(map)

geolocater = Nominatim(user_agent="tutorial")
for index, row in df.iterrows():
    try:
        location = geolocater.geocode(row["Home"])
        if location.latitude is not None:
            folium.Marker(
                location=[location.latitude, location.longitude],
                popup=f"""
                <table>
                    <tr>
                        <th>Date</th>
                        <th>Owner</th>
                        <th>Home</th>
                        <th>Product</th>
                        <th>Rep</th>
                        <th>Price</th>
                    </tr>
                    <tr>
                        <td>{row["Date"]}</td>
                        <td>{row["Owner"]}</td>
                        <td>{row["Home"]}</td>
                        <td> {row["Product"]}</td>
                        <td>{row["Rep"]}</td>
                        <td>{row["Price"]}</td>
                    </tr>
                </table>
                """,
                tooltip=f'Project # {row["Project #"]}'
            ).add_to(map)
    except:
        pass
        
map

# %%
# Save map
map.save('power-SE-MI.html')