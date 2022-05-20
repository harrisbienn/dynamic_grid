"""
NAME:           mapper.py

COMPATIBILITY:  Python 3.10

DESCRIPTION:    This program allows the user to draw a bounding box polygon using a mapping interface and
                and generate a .geojson file for input into the geojsonintake.py function

TO RUN:
    -   No special instructions

DATA FORMAT:    Standalone script

REQUIRES:       os, folium, geopandas, webbrowser

TODO:           N/A

AUTHOR:         Harris Bienn

ORGANIZATION:   The Water Institute of The Gulf

CONTACT:        hbienn@thewaterinstitute.org
"""

import os
import folium
from folium import plugins, features
import geopandas as gpd
import webbrowser


def mapper():
    # Import bounding box guides
    url = "https://github.com/hbienn/FoliumMapper/blob/main/precomputedbb/"
    gridbb_formatted = f"{url}/gridbb_formatted_wgs84.zip?raw=true"
    gridbb = gpd.read_file(gridbb_formatted)

    # Create a map object with coordinates centered on Baton Rouge, LA.
    m = folium.Map(location=[30.432555, -91.192306],
                   tiles="CartoDB positron",
                   zoom_start=8,
                   control_scale=True
                   )

    # Enable inset map
    insetmap = plugins.MiniMap(position='bottomright')
    m.add_child(insetmap)

    # Display cursor coordinates on screen
    cformat = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
    plugins.MousePosition(position='bottomleft',
                          separator=' | ',
                          prefix="Mouse:",
                          lat_formatter=cformat,
                          lng_formatter=cformat
                          ).add_to(m)

    # Enable geolocation search
    plugins.Geocoder(position='topright',
                     addmarker=True
                     ).add_to(m)

    # Enable latitude and longitude popups with mouse click
    features.LatLngPopup().add_to(m)

    # Allow map to be made full screen
    plugins.Fullscreen(position="topright",
                       title="Make fullscreen",
                       title_cancel="Exit fullscreen",
                       force_separate_button=True,
                       ).add_to(m)

    # Allow user to draw polygon and export bounding box and geojson
    plugins.Draw(export=True,
                 filename="boundingbox.geojson",
                 position="topleft",
                 draw_options={"rectangle": {'allowIntersection': False}},
                 edit_options={"poly": {'allowIntersection': False}}
                 ).add_to(m)

    '''
    # Add additional basemaps and enable layer control
    folium.LayerControl().add_to(m)
    folium.TileLayer('OpenStreetMap').add_to(m)
    folium.TileLayer('Stamen Terrain').add_to(m)
    folium.TileLayer('Stamen Toner').add_to(m)
    folium.TileLayer('Cartodb positron').add_to(m)
    folium.TileLayer('cartodb dark_matter').add_to(m)
    '''

    # Set tooltip prompt
    tooltip = "Select for attributes"

    # Enable popups
    popup = features.GeoJsonPopup(fields=["ID", "S", "W", "N", "E", "Download"],
                                  labels=True
                                  )

    # Force vector style manipulations
    folium.GeoJson(gridbb,
                   highlight_function=lambda feature: {
                       "stroke": True,
                       "color": '#006EFF',
                       "weight": 3,
                       "fill": True,
                       "fillColor": '#B39200',
                       "FillOpacity": 1,
                   },
                   style_function=lambda feature: {
                       "stroke": True,
                       "color": '#ffcf01',
                       "weight": 3,
                       "fill": True,
                       "fillColor": '#004CA8',
                       "FillOpacity": 0.5,
                   },
                   zoom_on_click=True,
                   popup=popup,
                   tooltip=tooltip,
                   ).add_to(m)

    # Display the map
    m.save("mapper.html")
    webbrowser.open_new_tab("file://" + os.path.realpath("mapper.html"))


if __name__ == "__main__":
    mapper()
