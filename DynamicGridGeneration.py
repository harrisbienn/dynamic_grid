"""
NAME:           backpackgrid.py

COMPATIBILITY:  Python 3.10

DESCRIPTION:    This program creates a regularly spaced grid of points from x,y points for the lower left hand and upper
right hand corners of a rectangular domain at a user specified grid resolution. Outputs as nparray and plaintext.

TO RUN:
    -   Run mapper.py to create a .geojson of the bounding polygon you want to generate a grid for.
        Keep it in the downloads directory on your local drive
    -   Modify function values as desired. Default variable assignments:
          -  in_path - attempts to locate "boundingbox.geojson" in your downloads folder
          -  out_path - saves "grid.csv" to your documents folder
          -  in_proj = 4326 - EPSG id for WGS84 geographic coordinate system with units in degrees
                (https://epsg.io/4326)
          -  out_proj = 26915 - EPSG id for NAD83 UTM 15N projected coordinate system with units in meters
                (https://epsg.io/26915)
          -  grid_spacing = 500 - assigned as the default grid spacing in meters
          -  grid_nparray - modify to change the variable name of the numpy array output grid
    -   Run the code

DATA FORMAT:    Manual input

REQUIRES:       os, pathlib, geopandas, pyproj, shapely, numpy

TODO:           1) implement polygon generation

AUTHOR:         Harris Bienn

ORGANIZATION:   The Water Institute of The Gulf

CONTACT:        hbienn@thewaterinstitute.org

"""

# Import Modules
import os
from pathlib import Path
import geopandas as gpd
from pyproj import CRS, Transformer
import shapely.geometry as geo
import numpy as np


# Define Formatting Classes
class c:
    C = '\033[96m'
    DC = '\033[36m'
    B = '\033[94m'
    G = '\033[92m'
    R = '\033[91m'
    BD = '\033[1m'
    UL = '\033[4m'
    END = '\033[0m'


in_path = str(os.path.join(Path.home(), "Downloads") + "\\boundingbox.geojson")
out_path = str(os.path.join(Path.home(), "Documents") + "\\grid.csv")
in_epsg = 4326
out_epsg = 26915
grid_spacing = 500

# Inform directory location of selected file
print("The directory location of the file you have selected is:", "\n")
print(c.BD + in_path + c.END, "\n")
input("Press Enter to continue...")

# Read GeoJSON into GeoDataFrame and make copy for geometry conversion
gdf = gpd.read_file(in_path)

print("Your input represented as a GeoDataFrame:", "\n")
print(c.BD + str(gdf) + c.END, "\n")
input("Press Enter to continue...")

# Define input and output coordinate systems
in_proj = CRS.from_user_input(in_epsg)
out_proj = CRS.from_user_input(out_epsg)

print("YOUR" + c.BD + c.C + " INPUT " + c.END + "COORDINATE SYSTEM IS: "
      + c.BD + c.R + str(in_proj) + c.END, "\n")
print(c.C + str(in_proj.to_wkt(pretty=True)) + c.END, "\n")
print("YOUR" + c.BD + c.B + " OUTPUT " + c.END + "COORDINATE SYSTEM IS: "
      + c.BD + c.R + str(out_proj) + c.END, "\n")
print(c.B + str(out_proj.to_wkt(pretty=True)) + c.END, "\n")
input("Press Enter to continue...")

# Grid resolution messages
print("You have selected " + c.BD + c.R + str(grid_spacing) + c.END +
      " meters as your desired grid resolution" + c.END, "\n")
input("Press Enter to continue...")

# Turn bounding box polygon vertices into points
bounds = gdf.bounds  # Returns tuple minx, miny, maxx, maxy of bounding box

print("Your bounding box's minimum and maximum latitudinal and longitudinal values are:", "\n")
print(bounds, "\n")

# Detail corners and convert to shapely point geometry
bounds = np.array(bounds)
sw = geo.Point((bounds[0, 0], bounds[0, 1]))
nw = geo.Point((bounds[0, 0], bounds[0, 3]))
ne = geo.Point((bounds[0, 2], bounds[0, 3]))
se = geo.Point((bounds[0, 2], bounds[0, 1]))

print(c.UL + "Points located at the SOUTHWEST and NORTHEAST corners of your bounding box will be " +
      "used to generate the grid." + c.END, "\n")
print("The updated geometry and location for the SOUTHWEST point of your bounding box is:", c.BD + c.G +
      str(sw) + c.END, "\n")
print("The updated geometry and location for the NORTHEAST point of your bounding box is:", c.BD + c.G +
      str(ne) + c.END, "\n")
input("Press Enter to continue...")

# Define coordinate system for transformer
transformer = Transformer.from_crs(in_proj, out_proj, always_xy=True)

print(c.UL + "Function will now transform p from", str(in_proj), "to", str(out_proj) + c.END, "\n")

# Transform corners to target CRS
transformed_sw = transformer.transform(sw.x, sw.y)  # Transforms SW corner point to 26915
transformed_ne = transformer.transform(ne.x, ne.y)  # Transforms SE corner point to 26915

print("The transformed location for the SOUTHWEST point of your grid is:", c.BD + c.G +
      str(transformed_sw) + c.END, "\n")
print("The transformed location for the NORTHEAST point of your grid is:", c.BD + c.G +
      str(transformed_ne) + c.END, "\n")
input("Press Enter to continue...")

# Iterate points over 2D area
print("Iterating grid starting at" + c.BD + " SOUTHWEST " + c.END + "origin point at a resolution of "
      + c.BD + c.R + str(grid_spacing) + c.END + " meters.", "\n")
grid_points = []
x = transformed_sw[0]
while x < transformed_ne[0]:
    y = transformed_sw[1]
    while y < transformed_ne[1]:
        p = geo.Point(x, y)
        grid_points.append(p)
        y += int(grid_spacing)
    x += int(grid_spacing)

# Create numpy array output
print("Beginning array generation.", "\n")
list_array = []
for pp in grid_points:
    list_array.append([pp.x, pp.y])
grid_nparray = np.array(list_array)

print(c.UL + "Array generation complete:" + c.END, "\n")
print(grid_nparray)
print("Your output can be called by via the " + c.BD + "grid_np_array" + c.END + " variable", "\n")
input("Press Enter to continue...")

# Create plaintext output
with open(out_path, 'w') as of:
    of.write('easting,northing\n')
    for p in grid_points:
        of.write('{:f},{:f}\n'.format(p.x, p.y))

print(c.BD + c.G + "Grid generation complete" + c.END)
