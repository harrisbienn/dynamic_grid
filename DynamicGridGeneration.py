"""
Name:           generateregulargrid.py
Compatibility:  Python 3.10
Description:    This program creates a regularly spaced grid of points from x,y points for the lower left hand and upper
right hand corners of a rectangular domain at a user specified grid resolution.

TO RUN:
    - Modify values in the Input section
    - Run the code

DATA FORMAT:    Manual input

Requires:       pyproj, shapely, numpy

ToDo:           1) implement polygon generation

AUTHOR:         Harris Bienn
ORGANIZATION:   The Water Institute of The Gulf
Contact:        hbienn@thewaterinstitute.org

"""

from pyproj import CRS, Transformer
import shapely.geometry as geo
import numpy as np

# ** INPUTS **
in_crs = CRS("EPSG:4326")  # EPSG:4326 (WGS84, Geographic, units in degrees) - https://epsg.io/4326
proj_crs = CRS("EPSG: 26915")  # EPSG:26915 (Projected, NAD83, units in meters) - https://epsg.io/26915
sw = geo.Point((-91.0, 29.0))  # Create corners of rectangle to be transformed to a grid
ne = geo.Point((-89.0, 31.0))  # units should be same as input to transformer
grid_spacing: int = 100  # Grid resolution in meters
out_path = r'Z:\Documents\ArcGIS\Projects\Smartport\grid_output2.csv'


# *** FUNCTIONS ***
# Define coordinate system for transformer
transformer = Transformer.from_crs(in_crs, proj_crs, always_xy=True)

# Transform corners to target CRS
transformed_sw = transformer.transform(sw.x, sw.y)  # Transform SW corner point to 26915
transformed_ne = transformer.transform(ne.x, ne.y)  # Transform SE corner point to 26915

# Iterate points over 2D area
grid_points = []
x = transformed_sw[0]
while x < transformed_ne[0]:
    y = transformed_sw[1]
    while y < transformed_ne[1]:
        points = geo.Point(x, y)
        grid_points.append(points)
        y += grid_spacing
    x += grid_spacing

#  Create numpy array output
list_array = []
for pp in grid_points:
    list_array.append([pp.x, pp.y])
nparray = np.array(list_array)

# Create text-based output
with open(out_path, 'w') as of:
    of.write('easting,northing\n')
    for points in grid_points:
        of.write('{:f},{:f}\n'.format(points.x, points.y))

# Iterate polygons over 2D area
# grid_polygons = []
# x2 = transformed_sw[0]
# while x2 < transformed_ne[0]:
#    y2 = transformed_sw[1]
#    while y2 < transformed_ne[1]:
#        polygons = geo.Polygon(x2, y2)
#        grid_polygons.append(polygons)
#        y2 += step_size
#    x2 += step_size

# with open(out_path + grid_name + '_polygon', 'w') as of:
#    of.write('lon,lat\n')
#    for polygons in grid_polygons:
#        of.write('{:f},{:f}\n'.format(polygons.x2, polygons.y2))
