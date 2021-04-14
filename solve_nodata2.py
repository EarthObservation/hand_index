import numpy as np
import rasterio
from pyproj.crs import CRS

# Paths
# source_hand = "c:\\Users\\ncoz\\ARRS_susa\\slo_06_new\\dem_slo_06_HAND_nc_NEW_fill500_600.tif"
source_hand = "c:\\Users\\ncoz\\ARRS_susa\\slo_06_new\\hand_index_d96tm.tif"
# result_hand = "c:\\Users\\ncoz\\ARRS_susa\\slo_06_new\\hand_index_d96tm.tif"
result_hand = "c:\\Users\\ncoz\\ARRS_susa\\slo_06_new\\hand_index_d96tm_LZW.tif"
nodata_mask = "c:\\Users\\ncoz\\ARRS_susa\\dmv_10m_nd999.tif"

with rasterio.open(source_hand) as ds:
    grid_a = ds.read(1)
    profile = ds.profile

# with rasterio.open(nodata_mask) as ds:
#     grid_b = ds.read(1)
#
# grid_a[grid_b == -999] = -999

# Update metadata
slo_crs = CRS.from_epsg(3794)
profile.update({"crs": slo_crs, "nodata": -999, "compress": 'LZW'})

# Save
with rasterio.open(result_hand, "w", **profile) as dst:
    dst.write(grid_a, 1)

print("DONE!")
