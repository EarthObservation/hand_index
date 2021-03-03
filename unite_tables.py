"""
Combines multiple SHP files into a single file (append columns and sort)
"""

import glob
import geopandas as gpd
from os.path import dirname, join, basename


def movecol(df, cols_to_move, ref_col='', place='After'):
    cols = df.columns.tolist()
    if place == 'After':
        seg1 = cols[:list(cols).index(ref_col) + 1]
        seg2 = cols_to_move
    elif place == 'Before':
        seg1 = cols[:list(cols).index(ref_col)]
        seg2 = cols_to_move + [ref_col]
    else:
        seg1 = None
        seg2 = None

    seg1 = [i for i in seg1 if i not in seg2]
    seg3 = [i for i in cols if i not in seg1 + seg2]

    return gpd.GeoDataFrame(df[seg1 + seg2 + seg3])


# # Read subset for debugging
# def read_100(shp_file, idx_list):
#     with fiona.open(shp_file) as src:
#         # dfs = [gpd.read_file(a) for a in shapes]
#         df = gpd.GeoDataFrame.from_features([src[x] for x in idx_list])
#     return df
#
#
# df1 = read_100(shapes[0], list(range(100)))  # right
# df2 = read_100(shapes[1], list(range(100)))  # left

# Location of all files
shapes = glob.glob("c:\\Users\\ncoz\\ARRS_susa\\drought_indices\\ZV2017*.shp")

# Read first data frame
print(f"Reading df0...")
df0 = gpd.read_file(shapes[0])

for pth in shapes[1:]:
    tf = basename(pth)
    print(f"Reading {tf}")
    df2 = gpd.read_file(pth)
    selected_index = tf[-8:-4] + "_mean"
    filtr = [selected_index, "GERK_PID", "POLJINA_ID"]
    print("Merging with df0...")
    df0 = df2[filtr].merge(df0, how='inner', on=["GERK_PID", "POLJINA_ID"])

# Reorder columns
df0 = movecol(
    df0,
    cols_to_move=['ndvi_mean', 'evi2_mean', 'ndwi_mean', 'savi_mean'],
    ref_col='hand_mean',
    place='Before'
)

dir_out = dirname(shapes[0])
out_name = "ZV2017_d96tm_Slo_big10_all"

# Save shapefile (drop GeoJSON and raster columns)
print("Saving SHP...")
out_shp = join(dir_out, out_name + ".shp")
df0.to_file(out_shp)

# Save CSV (also drop geometry)
print("Saving CSV...")
out_csv = join(dir_out, out_name + ".csv")
df0 = df0.drop(columns=["geometry"])
df0.to_csv(out_csv)


