import rasterio
import numpy as np
from pyproj.crs import CRS


# Assign CRS from pyproj
slo_crs = CRS.from_epsg(3794)

# Burn values into sinks of a conditioned DEM
# Create output raster
output_file = "c:\\Users\\ncoz\\ARRS_susa\\slo_06\\dem_slo_06_cond_nosink.tif"

# Open rasters
src_a = rasterio.open("c:\\Users\\ncoz\\ARRS_susa\\slo_06\\dem_slo_06_cond.tif")
# src_b = rasterio.open(streams.tif())
src_c = rasterio.open("c:\\Users\\ncoz\\ARRS_susa\\slo_06\\sinks_slo_06.tif")

grid_a = src_a.read(1)
# grid_b = src_b.read(1)
grid_c = src_c.read(1)

print(grid_a.shape)
# print(grid_b.shape)
print(grid_c.shape)

# Set nan
grid_a[grid_a < 0] = np.nan
# Get a list of all sinks
all_sinks = np.where(grid_c == 1)
# Get 3x3 grains
grains = [grid_a[a-1:a+2, b-1:b+2] for a, b in zip(all_sinks[0], all_sinks[1])]
# Calculate value to be inserted into dem
new_value = [np.nanmin(a) - 0.5 for a in grains]
# Insert value into grid_a
grid_a[all_sinks] = new_value
# Convert nodata to -999
grid_a[np.isnan(grid_a)] = -999

# Prepare metadata & save
out_meta = src_a.profile.copy()
out_meta.update({"crs": slo_crs, "nodata": -999})
with rasterio.open(output_file, "w", **out_meta) as dest:
    dest.write(grid_a, 1)

src_a.close()
# src_b.close()
src_c.close()

print("DONE!")
