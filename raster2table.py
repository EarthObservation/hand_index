import time
from tqdm import tqdm

from shapely.geometry import mapping
import numpy as np
import geopandas as gpd
import rasterio
from rasterio.mask import mask
from os.path import join, basename


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
        out_image, _ = mask(raster, geom, crop=True, all_touched=True)
        return out_image

    # Prepare output name for saving results to files
    out_name = basename(pth_shp)[:-4] + suffix

    # Read polygons to data frame
    print("Reading shapefile...")
    t = time.time()
    tdf = gpd.read_file(pth_shp)
    t = time.time() - t
    print(f"Read SHP with GeoPandas: {t} seconds")

    # # Write to / read from pickle for faster debugging
    # pickle.dump(tdf, "df.p", "wb"))
    # tmp_read = pickle.load(open("df.p", "rb"))

    # Reformat geometry to GeoJSON format (append a new column)
    tqdm.pandas(desc="geometry -> GeoJSON")
    tdf["geom"] = tdf.geometry.progress_apply(lambda g: [mapping(g)])

    # # Uncomment for processing of a subset (useful for debugging)
    # tdf = tdf[tdf.REGIJA == 1].copy()

    # Extract rasters, and calculate mean & std (each stored to a new column)
    src = rasterio.open(pth_raster)
    tqdm.pandas(desc="Extracting arrays")
    tdf["hand_rst"] = tdf.geom.progress_apply(lambda g: ms_rio(g, src))
    tqdm.pandas(desc="Mean")
    tdf["hand_mean"] = tdf.hand_rst.progress_apply(lambda g: np.nanmean(g))
    tqdm.pandas(desc="Std")
    tdf["hand_std"] = tdf.hand_rst.progress_apply(lambda g: np.nanstd(g))
    src.close()

    # Save shapefile (drop GeoJSON and raster columns)
    print("Saving SHP...")
    out_shp = join(dir_out, out_name + ".shp")
    tdf = tdf.drop(columns=["geom", "hand_rst"])
    tdf.to_file(out_shp)

    # Save CSV (also drop geometry)
    print("Saving CSV...")
    out_csv = join(dir_out, out_name + ".csv")
    tdf = tdf.drop(columns=["geometry"])
    tdf.to_csv(out_csv)

    return "DONE!"


if __name__ == "__main__":
    # SET PATHS
    # ---------
    # Input raster
    geotiff = "c:\\Users\\ncoz\\ARRS_susa\\fill_tif_fill\\dem_slo_03_HAND_fill_nan.tif"
    # Input shape file
    shapefile = "c:\\Users\\ncoz\\ARRS_susa\\poline\\ZV2017_d96tm.shp"
    # Output folder and suffix to be added to SHP and CSV files
    output_loc = "c:\\Users\\ncoz\\ARRS_susa\\poline"
    suff = "_hand"

    result = r2t(geotiff, shapefile, output_loc, suff)
    print(result)
