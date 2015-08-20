from __future__ import print_function
import requests
import h5py
import os
import numpy
from PIL import Image
import time

from enums import *
from Request import *


def put_data(server=DEFAULT_SERVER, token, data, x_start, x_stop=0, y_start, y_stop=0, z_start, z_stop=0, filename="tmp.hdf5"):
    """
    Upload data onto the OCP server.

    Arguments:
        :server:        ``string : ocpy.access.enums.DEFAULT_SERVER`` The server to access
        :token:         ``string`` The token to upload (must be read/write)
        :data:          ``numpy.ndarray`` The data to upload
        :q_start:       ``int`` Lower bound of Q dimension
        :q_stop:        ``int : 0`` Upper bound of Q dimension. If omitted, is
                        autopopulated to contain q_start + data-size.
        :filename:      A temporary HDF5 file to stream to the server.

    Returns:
        : bool : Success of the call (True/False).
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
