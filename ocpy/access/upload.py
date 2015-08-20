from __future__ import print_function
import requests
import h5py
import os
import numpy
from PIL import Image
import time

from enums import *
from Request import *


def put_data(token, data, x_start, x_stop=0, y_start, y_stop=0, z_start, z_stop=0, filename):
    """
    Upload data onto the OCP server.
    """

    if x_stop == 0: x_stop = x_start + data.shape[0]
    if y_stop == 0: y_stop = y_start + data.shape[1]
    if z_stop == 0: z_stop = z_start + data.shape[2]

    if (x_stop - x_start) != data.shape[0]:
        raise DataSizeError("Bad fit: x-range")
    if (y_stop - y_start) != data.shape[1]:
        raise DataSizeError("Bad fit: y-range")
    if (z_stop - z_start) != data.shape[2]:
        raise DataSizeError("Bad fit: z-range")

    fout = h5py.File(filename, driver="core", backing_store=True)
    fout.create_dataset("CUTOUT", data.shape, data.dtype, compression="gzip", data=data)
    fout.close()

    req = Request(
        token =         token,
        x_start =       x_start,
        x_stop =        x_stop,
        y_start =       y_start,
        y_stop =        y_stop,
        z_start =       z_start,
        z_stop =        z_stop,
        resolution =    "1",
        format =        "hdf5"
    )

    url = req.to_url()

    with open(filename, 'rb') as payload:
        req = requests.post(url, data=payload)

    return req.status_code == 200
