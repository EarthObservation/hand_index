import numpy as np
import rasterio
from pyproj.crs import CRS

# Paths
source_dem = "d:\\nejc\\hand_index\\dmv_10m.tif"
result_dem = "d:\\nejc\\hand_index\\dmv_10m_nd999.tif"

with rasterio.open(source_dem) as ds:
    array = ds.read()
    profile = ds.profile

    # Find missing value
    d_x, d_y = (38203, -141588)
    x, y = (ds.bounds.left + d_x, ds.bounds.top + d_y)
    row, col = ds.index(x, y)
    nan_val = array[0, row, col]

# Change nan values to -999
array[np.isnan(array)] = -999
array[array == 0] = -999

# Update metadata
slo_crs = CRS.from_epsg(3794)
profile.update({"crs": slo_crs, "nodata": -999})

# Save
with rasterio.open(result_dem, "w", **profile) as dst:
    dst.write(array)

print("DONE!")