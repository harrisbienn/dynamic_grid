# SmartPort Dynamic Grid Generation
COMPATIBILITY:  Python 3.10

DESCRIPTION:    This repo contains scripts that help create a regularly spaced grid of points from x,y points for the lower left hand and upper
right hand corners of a rectangular domain at a user specified grid resolution. Outputs as nparray and plaintext.

TO RUN:

    -   Code can be run as a module by running gridinit_basic.py or gridinit.py (dependent on console.py, pocketgrid.py, and mapper.py). 

    -   Modify function values as desired. Default variable assignments:
          
          -  in_path - attempts to locate "boundingbox.geojson" in your downloads folder
          
          -  out_path - saves "grid.csv" to your documents folder
          
          -  in_proj = 4326 - EPSG id for WGS84 geographic coordinate system with units in degrees
                (https://epsg.io/4326)
          
          -  out_proj = 26915 - EPSG id for NAD83 UTM 15N projected coordinate system with units in meters
                (https://epsg.io/26915)
          
          -  grid_spacing = 500 - assigned as the default grid spacing in meters
    
    -   Run the code

AUTHOR:         Harris Bienn

ORGANIZATION:   The Water Institute of The Gulf

CONTACT:        hbienn@thewaterinstitute.org
