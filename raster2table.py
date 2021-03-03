import time
from tqdm import tqdm

from shapely.geometry import mapping
import numpy as np
import geopandas as gpd
import rasterio
from rasterio.mask import mask
from os.path import join, basename
from os import makedirs


def r2t(pth_raster, pth_shp, dir_out, suffix):
    """Function creates shape file and csv file containing mean and standard
    deviation of the underlain raster for each polygon.

    Parameters
    ----------
    pth_raster : str
        Path to input raster.
    pth_shp : str
        Path to input shapefile.
    dir_out : str
        Path to directory for saving results.
    suffix : str
        Suffix to be added to results.

    Returns
    -------
        Finished message.
    """

    def ms_rio(geom, raster):
        """Returns subset of an array covered by the input polygon. The input
        polygon has to be in the GeoJSON format. The crop attribute sets values
        not covered by polygon to nan. All_touched is used to prevent empty rasters
        for very thin polygons."""
        out_image, _ = mask(raster, geom, crop=True, all_touched=True, nodata=np.nan)
        return out_image

    # Prepare output name for saving results to files
    out_name = basename(pth_shp)[:-4] + "_" + suffix

    # Read polygons to data frame
    print("Reading shapefile...")
    t = time.time()
    tdf = gpd.read_file(pth_shp)
    t = time.time() - t
    print(f"Read SHP with GeoPandas: {t} seconds")

    # # Write to / read from pickle for faster debugging
    # pickle.dump(tdf, "df.p", "wb"))
    # tmp_read = pickle.load(open("df.p", "rb"))

    # # Uncomment for processing of a subset (useful for debugging)
    # # tdf = tdf[tdf.REGIJA == 4].copy()
    # tdf = tdf[0:1000].copy()

    # Reformat geometry to GeoJSON format (append a new column)
    tqdm.pandas(desc="geometry -> GeoJSON")
    tdf["geom"] = tdf.geometry.progress_apply(lambda g: [mapping(g)])

    # Extract rasters, and calculate mean & std (each stored to a new column)
    src = rasterio.open(pth_raster)
    tqdm.pandas(desc="Extracting arrays")
    tdf["hand_rst"] = tdf.geom.progress_apply(lambda g: ms_rio(g, src))
    src.close()

    # Calculate mean by dates
    tqdm.pandas(desc="Mean by dates")
    tdf["by_dates"] = tdf.hand_rst.progress_apply(lambda g: np.nanmean(g, axis=(1, 2)))
    print(" Splitting LIST to COLUMNS...")
    # Create list of column names (dates of individual images)
    with open("c:\\susa\\datumi_ZV2017.txt") as file:
        # TODO: Here check if dates are correctly created
        dates = [suffix + "_" + x.rstrip('\n') for x in file]
    tdf[dates] = gpd.GeoDataFrame(tdf.by_dates.tolist(), index=tdf.index)
    tdf = tdf.drop(columns=["by_dates"])

    # # Calculate aggregated mean
    # tqdm.pandas(desc="Mean")
    # index_tag = suffix + "_mean"
    # tdf[index_tag] = tdf.hand_rst.progress_apply(lambda g: np.nanmean(g))

    # Caluclate Standard Deviation (HAND INDEX)
    # tqdm.pandas(desc="Std")
    # tdf["hand_std"] = tdf.hand_rst.progress_apply(lambda g: np.nanstd(g))

    # Save shapefile (drop GeoJSON and raster columns)
    print("Saving SHP...")
    makedirs(dir_out, exist_ok=True)
    out_shp = join(dir_out, out_name + ".shp")
    tdf = tdf.drop(columns=["geom", "hand_rst"])
    tdf.to_file(out_shp)

    # Save CSV (also drop geometry)
    print("Saving CSV...")
    makedirs(dir_out, exist_ok=True)
    out_csv = join(dir_out, out_name + ".csv")
    tdf = tdf.drop(columns=["geometry"])
    tdf.to_csv(out_csv)

    return "DONE!"


if __name__ == "__main__":
    # SET PATHS
    # ---------
    # Input raster
    geotiff = "c:\\susa\\ZV2017_NDVI_Cmask.tif"
    # geotiff = "c:\\Users\\ncoz\\ARRS_susa\\fill_tif_fill\\dem_slo_03_HAND_fill_nan.tif"
    # Input shape file
    # shapefile = "c:\\susa\\ZV2017_d96tm_Slo_big10\\ZV2017_d96tm_Slo_big10.shp"
    shapefile = "c:\\susa\\ZV2017_susni_indeksi\\ZV2017_d96tm_Slo_big10_ndvi.shp"
    # Output folder and suffix to be added to SHP and CSV files
    output_loc = "c:\\susa\\ZV2017_susni_indeksi_ts"
    suff = "ndvi"

    print(f">>> Run for: {suff}")

    result = r2t(geotiff, shapefile, output_loc, suff)
    print(result)
