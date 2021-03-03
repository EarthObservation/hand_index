import geopandas as gpd
from os.path import join

index = "evi2"

# Target size
slo = gpd.read_file("c:\\susa\\ZV2017_d96tm_Slo_big10\\ZV2017_d96tm_big10_slo_all.shp")

# Input file
filter_dir = "c:\\susa\\ZV2017_susni_indeksi_ts"
filter_name = f"ZV2017_d96tm_Slo_big10_{index}_{index}.shp"
to_filter = join(filter_dir, filter_name)

# Output file
save_dir = r"c:\susa\ZV2017_susni_indeksi_SLO_ts"
save_name = f"ZV2017_d96tm_big10_slo_ts_{index}.shp"
save_file = join(save_dir, save_name)

# Read gdf:
gdf = gpd.read_file(to_filter)

keys = ["GERK_PID", "POLJINA_ID"]

i1 = gdf.set_index(keys).index
i2 = slo.set_index(keys).index
gdf = gdf[i1.isin(i2)]

# Save shapefile (drop GeoJSON and raster columns)
print("Saving SHP...")
gdf.to_file(save_file)

# Save CSV (also drop geometry)
print("Saving CSV...")
gdf2 = gdf.drop(columns=["geometry"])
gdf2.to_csv(save_file[:-4] + ".csv")
