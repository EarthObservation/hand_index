"""
This script is used for identifying sinks, that will be used in the creation
of the HAND index for Slovenia.
"""

import geopandas as gpd


# Path to nodes (river end points)
pth_nodes = ""
gdf_nodes = gpd.read_file(pth_nodes)

# Path to point layer (containing sinks)
pth_sinks = "c:\\Users\\ncoz\\ARRS_susa\\DRSV_HIDRO5_TC\\DRSV_HIDRO5_TC.shp"
gdf_sinks = gpd.read_file(pth_sinks)

