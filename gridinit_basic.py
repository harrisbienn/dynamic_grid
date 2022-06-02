import os
from pathlib import Path
from mapper import mapper
from pocketgrid import grid


def run():
    def map_open():
        map_open = input("Do you need to use the interactive map to generate a bounding box? (Y/N)")
        if map_open == "Y":
            print("\n",
                  "Draw a new bounding box and export it or select an precomputed one and save a copy in your downloads"
                  " folder.", "\n")
            mapper()
        return map_open
    map_open()

    input("Press enter to continue...")

    print("\n", "The grid generation function takes five (5) parameters:", "\n",
          "1) in_path         By default the function attempts to locate "'boundingbox.geojson'" in your downloads "
          "folder.",
          "\n",
          "                   This parameter will accept any *.geojson as input if it is provided as a properly "
          "formatted path.",
          "\n", "\n",
          "2) out_path        By default the function will save a "'grid.csv'" to your documents folder",
          "\n",
          "                   This parameter will accept any *.csv or *.txt if it is provided as a properly formatted "
          "path.",
          "\n", "\n",
          "3) in_epsg         Default value is 4326, the EPSG id for WGS84 geographic coordinate system with units in "
          "degrees (https://epsg.io/4326).",
          "\n",
          "                   This parameter will accept any numeric EPSG identifier so long as there is a associated "
          "listing and transformation available in the PROJ database.",
          "\n", "\n",
          "4) out_epsg        Default value is 26915 - EPSG id for NAD83 UTM 15N projected coordinate system with "
          "units in meters (https://epsg.io/26915).",
          "\n",
          "                   This parameter will accept any numeric EPSG identifier so long as there is a associated "
          "listing and transformation available in the PROJ database.",
          "\n", "\n",
          "5) grid_spacing    The grid functions defaults to a grid spacing of 500 meters but can be user modified if "
          "the input is provided as an integer",
          "\n", "\n")

    input("Press Enter to continue...")

    def input_mod():
        input_mod = input("Would you like to specify a different input path than the default value? (Y/N)")
        if input_mod == "Y":
            in_path = input("Enter the fully formatted path to your input .geojson.")
        else:
            in_path = str(os.path.join(Path.home(), "Downloads") + "\\boundingbox.geojson")
        return in_path

    in_path = input_mod()

    def output_mod():
        output_mod = input("Would you like to specify a different output path than the default value? (Y/N)")
        if output_mod == "Y":
            out_path = input("Enter the fully formatted path to your output .txt or .csv.")
        else:
            out_path = str(os.path.join(Path.home(), "Documents") + "\\grid.csv")
        return out_path

    out_path = output_mod()

    def in_epsg_mod():
        in_epsg_mod = input(
            "Would you like to specify a different input coordinate system than the default value? (Y/N)")
        if in_epsg_mod == "Y":
            in_epsg = int(input("Enter the EPSG identifier of your desired coordinate system."))
        else:
            in_epsg = 4326
        return in_epsg

    in_epsg = in_epsg_mod()

    def out_epsg_mod():
        out_epsg_mod = input(
            "Would you like to specify a different output coordinate system than the default value? (Y/N)")
        if out_epsg_mod == "Y":
            out_epsg = int(input("Enter the EPSG identifier of your desired coordinate system."))
        else:
            out_epsg = 26915
        return out_epsg

    out_epsg = out_epsg_mod()

    def grid_mod():
        grid_mod = input("Would you like to specify a grid spacing than the default value? (Y/N)")
        if grid_mod == "Y":
            grid_spacing = int(input("Enter your desired grid spacing in meters."))
        else:
            grid_spacing = 500
        return grid_spacing

    grid_spacing = grid_mod()

    print("\n", "You have selected the following parameters as input:", "\n", "\n",
          "in_path = ", in_path, "\n",
          "out_path = ", out_path, "\n",
          "in_epsg = ", in_epsg, "\n",
          "out_epsg = ", out_epsg, "\n",
          "grid_spacing = ", grid_spacing, "\n")

    input("Press enter to run the grid generator with these values.")

    grid(in_path, out_path, in_epsg, out_epsg, grid_spacing)

    print("Grid generation complete")


if __name__ == "__main__":
    run()
