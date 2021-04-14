"""
IDEA 2: Testing the stacking of rasters. To be used for extraction of subsets of
raster covered by polygons.
"""
import rasterio
import numpy as np
import time
from os.path import dirname, join, basename
from os import makedirs
import glob


def stack_gtif(q_key, pth_out):
    t = time.time()

    file_list = sorted(glob.glob(q_key))

    bnds = len(file_list)

    # Read metadata of first file
    with rasterio.open(file_list[0]) as src0:
        meta = src0.meta
        shape = src0.shape

    # Update meta to reflect the number of layers
    meta.update(count=bnds)

    # # Read each layer and write it to stack (sightly slower 36 seconds)
    # dss = [rasterio.open(src) for src in file_list]
    # stack = [src.read() for src in dss]
    # stack = np.concatenate(stack, axis=0)

    # Read directly into array (was slightly faster 28 seconds)
    stack = np.empty((bnds, shape[0], shape[1]), meta["dtype"])
    dss = [rasterio.open(src) for src in file_list]
    for b, src in enumerate(dss):
        stack[b, :, :] = src.read(1)

    [src.close() for src in dss]

    makedirs(dirname(pth_out), exist_ok=True)
    with rasterio.open(pth_out, 'w', **meta) as dst:
        dst.write(stack)

    t = time.time() - t
    return f"Finished in: {t} seconds"


if __name__ == "__main__":
    # paths = [
    #     "c:\\Users\\ncoz\\ARRS_susa\\fill_tif_fill\\dem_slo_03_HAND_fill_nan.tif",
    #     "c:\\Users\\ncoz\\ARRS_susa\\dem_slo_02_HAND_final.tif",
    #     "c:\\Users\\ncoz\\ARRS_susa\\dem_slo_13_HAND_final.tif"
    # ]

    d_index = "SAVI"
    print(d_index)

    # path = "p:\\ARRS Susa\\podatki\\Sentinel-2_atm_10m_D96_2017_Slovenia"
    path = "c:\\Users\\ncoz\\ARRS_susa\\ms_stacked"
    file = f"*{d_index}_Cmask.tif"
    glob_keyword = join(path, file)

    # out_file = f"C:\\susa\\ZV2017_{d_index}_Cmask.tif"
    out_file = "c:\\Users\\ncoz\\ARRS_susa\\ms_stacked\\stacked.tif"

    out = stack_gtif(glob_keyword, out_file)
    print(out)
