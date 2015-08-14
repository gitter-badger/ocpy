"""
This script downloads 1GB of the bock11 dataset from OCP.
"""

import ocpaccess.download
import ocpaccess.convert.png
from ocpaccess.Request import *
import os, glob
import h5py


DATA_LOCATION = "bock11_sample"

starting_directory = os.getcwd()
#
# # Save downloaded files to the bock11_sample/ directory
# downloaded_files, failed_files = \
#         ocpaccess.download.get_data(
#                             token="bock11",        resolution=4,
#                             x_start=3000,           x_stop=3010,
#                             y_start=3000,           y_stop=3010,
#                             z_start=3100,           z_stop=3150,
#                             location=DATA_LOCATION)

os.chdir(DATA_LOCATION + "/hdf5")

for filename in glob.glob("*.hdf5"):
    # First get the actual parameters from the HDF5 file.
    req = Request(filename)
    i = req.z_start

    print("Slicing " + filename)
    f = h5py.File(filename, "r")
    # OCP stores data inside the 'cutout' h5 dataset
    data_layers = f.get('CUTOUT')

    out_files = []
    for layer in data_layers:
        # Filename is formatted like the request URL but `/` is `-`
        png_file = filename + str(i) + ".png"

        out_files.append(
            ocpaccess.convert.png.export_png("../png/" + png_file, numpy.array(layer)))
        i += 1

    # if you want, you have access to the out_files array here.
