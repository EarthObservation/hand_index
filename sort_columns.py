"""
Not a good code, but a quick fix to sort and rename columns into the correct order.

The reason why I had to do this was because images were not correctly stacked (wrong file order) for
ndvi and evi2 index. Changed code in stack_gtif to sort by filename (in our case filename is date,
so it is sorted by date).
"""

import geopandas as gpd
from os.path import join, basename

idx = "savi"

# src = "c:\\susa\\ZV2017_susni_indeksi_ts\\ZV2017_d96tm_Slo_big10_evi2_evi2 _FAIL.shp"
src = f"p:\\ARRS Susa\\podatki\\indeksi_big10_ts_slo\\ZV2017_d96tm_big10_ts_slo_{idx}.shp"

# Open shapefile
gdf = gpd.read_file(src)
keys = gdf.keys()
print(keys)
print("\nNumber of columns in SHP file:")
print(len(keys))

# Column names at the beginning that don't change
before = ['GERK_PID', 'RABA_ID', 'POVR_GERK_', 'POLJINA_ID', 'SIFRA_KMRS',
          'OBRAZEC', 'INTERSECT', 'POVR_ar', 'REGIJA', 'evi2_mean']

# # Current order of labels (olumn names) - we first need to rename the corrupted labels to these
# new_name = [
#     "evi2_2017-10-08",
#     "evi2_2017-02-20",
#     "evi2_2017-04-11",
#     "evi2_2017-04-21",
#     "evi2_2017-05-01",
#     "evi2_2017-05-11",
#     "evi2_2017-05-21",
#     "evi2_2017-05-31",
#     "evi2_2017-06-10",
#     "evi2_2017-06-20",
#     "evi2_2017-06-30",
#     "evi2_2017-07-10",
#     "evi2_2017-07-20",
#     "evi2_2017-07-30",
#     "evi2_2017-08-09",
#     "evi2_2017-08-19",
#     "evi2_2017-08-29",
#     "evi2_2017-09-08",
#     "evi2_2017-10-18",
#     "geometry"
# ]
# new_columns = before + new_name
# len(new_columns)

# Use this to rename columns in filtered (slo_ts) files (Somehow the name was corrupted)
new_name = ["savi_mean",
            "savi_2017-02-20", "savi_2017-04-11", "savi_2017-04-21", "savi_2017-05-01", "savi_2017-05-11",
            "savi_2017-05-21", "savi_2017-05-31", "savi_2017-06-10", "savi_2017-06-20", "savi_2017-06-30",
            "savi_2017-07-10", "savi_2017-07-20", "savi_2017-07-30", "savi_2017-08-09", "savi_2017-08-19",
            "savi_2017-08-29", "savi_2017-09-08", "savi_2017-10-08", "savi_2017-10-18"]
new_index = [idx + a[4:] for a in new_name]
new_columns = before[:-1] + new_index + ["geometry"]
print(f"Number of new labels: {len(new_columns)}")

# Set labels to the current columns
gdf2 = gdf.set_axis(new_columns, axis=1, inplace=False)
print(gdf2.keys())

# # Correct order of labels - reorder columns to match this pattern
# new_order = [
#     "evi2_2017-02-20",
#     "evi2_2017-04-11",
#     "evi2_2017-04-21",
#     "evi2_2017-05-01",
#     "evi2_2017-05-11",
#     "evi2_2017-05-21",
#     "evi2_2017-05-31",
#     "evi2_2017-06-10",
#     "evi2_2017-06-20",
#     "evi2_2017-06-30",
#     "evi2_2017-07-10",
#     "evi2_2017-07-20",
#     "evi2_2017-07-30",
#     "evi2_2017-08-09",
#     "evi2_2017-08-19",
#     "evi2_2017-08-29",
#     "evi2_2017-09-08",
#     "evi2_2017-10-08",
#     "evi2_2017-10-18",
#     "geometry"
# ]
# sort_columns = before + new_order

# # Reorder columns
# gdf2 = gdf2[sort_columns]
# print(gdf2.keys())

save_file = src[:-4] + "_popravljen.shp"

# Save shapefile (drop GeoJSON and raster columns)
print("Saving SHP...")
gdf2.to_file(save_file)

# # Save CSV (also drop geometry)
# print("Saving CSV...")
# gdf2 = gdf2.drop(columns=["geometry"])
# gdf2.to_csv(save_file[:-4] + ".csv")
