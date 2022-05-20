"""
NAME:           pocketgrid.py

COMPATIBILITY:  Python 3.10

DESCRIPTION:    Creates a regularly spaced grid of points from x,y points for the lower left hand and upper
right hand corners of a rectangular domain at a user specified grid resolution. Outputs as nparray and plaintext.

TO RUN:
    -   Run mapper.py to create a .geojson of the bounding polygon you want to generate a grid for.
        Keep it in the downloads directory on your local drive.
    -   Modify function values as desired. Default variable assignments:
          -  in_path - attempts to locate "boundingbox.geojson" in your downloads folder
          -  out_path - saves "grid.csv" to your documents folder
          -  in_epsg = 4326 - EPSG id for WGS84 geographic coordinate system with units in degrees
                (https://epsg.io/4326)
          -  out_epsg = 26915 - EPSG id for NAD83 UTM 15N projected coordinate system with units in meters
                (https://epsg.io/26915)
          -  grid_spacing = 500 - assigned as the default grid spacing in meters
    -   Run the code

DATA FORMAT:    Manual input

REQUIRES:       os, pathlib, geopandas, pyproj, shapely, numpy

TODO:           1) implement polygon generation

AUTHOR:         Harris Bienn

ORGANIZATION:   The Water Institute of The Gulf

CONTACT:        hbienn@thewaterinstitute.org

"""

import os
from pathlib import Path
import geopandas as gpd
from pyproj import CRS, Transformer
import shapely.geometry as geo
import numpy as np


def grid(in_path=str(os.path.join(Path.home(), "Downloads") + "\\boundingbox.geojson"),
         out_path=str(os.path.join(Path.home(), "Documents") + "\\grid.csv"),
         in_epsg=4326,
         out_epsg=26915,
         grid_spacing=500):
    gdf = gpd.read_file(in_path)  # Read GeoJSON into GeoDataFrame and make copy for geometry conversion
    in_proj = CRS.from_user_input(in_epsg)  # Define input coordinate system
    out_proj = CRS.from_user_input(out_epsg)  # Define output coordinate system
    bounds = np.array(gdf.bounds)  # Returns tuple minx, miny, maxx, maxy of bounding box
    sw = geo.Point((bounds[0, 0], bounds[0, 1]))  # Detail SW corner and convert to shapely point geometry
    ne = geo.Point((bounds[0, 2], bounds[0, 3]))  # Detail NE corner and convert to shapely point geometry
    transformer = Transformer.from_crs(in_proj, out_proj, always_xy=True)  # Define transformer
    transformed_sw = transformer.transform(sw.x, sw.y)  # Transforms SW corner point to target CRS
    transformed_ne = transformer.transform(ne.x, ne.y)  # Transforms SE corner point to target CRS
    grid_points = []
    list_array = []
    x = transformed_sw[0]
    while x < transformed_ne[0]:
        y = transformed_sw[1]
        while y < transformed_ne[1]:
            p = geo.Point(x, y)
            grid_points.append(p)
            y += int(grid_spacing)
        x += int(grid_spacing)
        for pp in grid_points:
            list_array.append([pp.x, pp.y])
    with open(out_path, 'w') as of:  # Create plaintext output
        of.write('easting,northing\n')
        for points in grid_points:
            of.write('{:f},{:f}\n'.format(points.x, points.y))
    grid_nparray = np.array(list_array)  # Create numpy array output
    return grid_nparray


grid_nparray = grid()


if __name__ == "__main__":
    grid()
