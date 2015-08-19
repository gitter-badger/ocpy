"""
This script downloads a few pixels from a few Kasthuri 2015 tokens.
"""

import ocpy.download
from ocpy.convert import png
from ocpy.Request import *
import os, glob
import h5py



def download_token_and_convert_to_png(tk):
    DATA_LOCATION = tk

    starting_directory = os.getcwd()

    # Save downloaded files to the bock11_sample/ directory
    downloaded_files, failed_files = \
            ocpy.download.get_data(
                                token=tk,               resolution=1,
                                x_start=3000,           x_stop=3010,
                                y_start=3000,           y_stop=3010,
                                z_start=100,            z_stop=150,
                                location=DATA_LOCATION)

    # Write error log
    with open(tk + '/errors', 'a') as f:
        for fail in failed_files:
            f.write(fail)

    os.mkdir(DATA_LOCATION + "/png")
    os.chdir(DATA_LOCATION + "/hdf5")

    for filename in glob.glob("*.hdf5"):
        # First get the actual parameters from the HDF5 file.
        req = Request(filename)
        i = int(req.z_start)

        print("Slicing " + filename)
        f = h5py.File(filename, "r")
        # OCP stores data inside the 'cutout' h5 dataset
        data_layers = f.get('CUTOUT')

        out_files = []
        for layer in data_layers:
            # Filename is formatted like the request URL but `/` is `-`
            png_file = filename + "." + str(i).zfill(6) + ".png"

            out_files.append(
                png.export_png("../png/" + png_file, layer))
            i += 1

        # if you want, you have access to the out_files array here.
    os.chdir(starting_directory)


download_token_and_convert_to_png('kasthuri11')
download_token_and_convert_to_png('kasthuri11cc')
