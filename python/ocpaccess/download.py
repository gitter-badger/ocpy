from __future__ import print_function
import requests
import h5py
import os
import numpy
from PIL import Image

import convert.tiff


DEFAULT_SERVER =    'http://openconnecto.me'
DEFAULT_FORMAT =    'hdf5'
DEFAULT_ZOOM   =    1
CHUNK_DEPTH    =    16


def get_info(token, server=DEFAULT_SERVER):
    """
    Get information about a dataset from its token, using the /info endpoint.

    Arguments:
        token:      The token identifying the dataset to investigate
    Returns:
        JSON object containing the content of the /info page.
    """
    url = '/'.join([server, 'ocp', 'ca', token, 'info', ''])
    req = requests.get(url)
    return req.json()


def get_data(token,
             x_start, x_stop,
             y_start, y_stop,
             z_start, z_stop,
             fmt=DEFAULT_FORMAT,
             zoom=DEFAULT_ZOOM,
             server=DEFAULT_SERVER,
             location="./",
             ask_before_writing=False):
    """
    Get data from the OCP server.

    Arguments:
        server:                 Internet-facing server
        token:                  Token to identify data to download
        fmt:                    The desired output format (see ocp_Convert repository to convert locally)
        zoom:                   Zoom level (starts at 0)
        Q_start:                   The lower bound of dimension 'Q'
        Q_stop:                   The upper bound of dimension 'Q'
        location:               The on-disk location where we'll create /hdf5 and /tiff
        ask_before_writing:     Ask (y/n) before creating directories.

    Returns:
        None
    """

    total_size = (x_stop - x_start) * (y_stop - y_start) * (z_stop - z_start) * (14./(1000.*1000.*16.))

    print("Downloading approximately " + str(total_size) + " MB.\n")

    # Figure out where we'll be saving files. If the directories don't
    # exist, let's create them now.
    location = location if location else os.getcwd()
    try:
        os.mkdir(location)
    except Exception as e:
        print("Directory /" + location + " already exists, not creating.")

    os.chdir(location)

    try:
        os.mkdir('hdf5'); os.mkdir('tiff');
    except Exception as e:
        print("Data directories already exist, not creating /hdf5 or /tiff.")

    if ask_before_writing:
        confirm = raw_input("The data will be saved to /" + location + ".\n" +
              "Continue? [yn] ")

        if confirm is 'n':
            return;

    fmt = "hdf5" # Hard-coded for now to minimize server-load

    # The array of local files that we create
    local_files = []

    # OCP stores cubes of z-size = CHUNK_DEPTH. To be efficient,
    # we'll download in CHUNK_DEPTH-z-slice units.
    if z_stop - z_start <= CHUNK_DEPTH:
        # We don't have to split, just download.
        local_files.append(
            _download_data(server, token, fmt, zoom,
                            x_start, x_stop,
                            y_start, y_stop,
                            z_start, z_stop, "hdf5")
        )
    else:
        # We need to split into CHUNK_DEPTH-slice chunks.
        z_last = z_start
        while z_last < z_stop:
            # Download from z_last to z_last + CHUNK_DEPTH OR
            # z_stop, whichever is smaller
            if z_stop <= z_last + CHUNK_DEPTH:
                # Download from z_last to z_stop
                local_files.append(
                    _download_data(server, token, fmt, zoom,
                            x_start, x_stop,
                            y_start, y_stop,
                            z_last, z_stop, "hdf5")
                )
            else:
                # Download from z_last to z_last + CHUNK_DEPTH
                local_files.append(
                    _download_data(server, token, fmt, zoom,
                            x_start, x_stop,
                            y_start, y_stop,
                            z_last, z_last + CHUNK_DEPTH, "hdf5")
                )

            z_last += CHUNK_DEPTH + 1

    # We now have an array, `local_files`, holding all of the
    # files that we downloaded.
    # print([i for i in local_files])
    convert_files_to_tiff(token, fmt, zoom, x_start, x_stop, y_start, y_stop, local_files)


def convert_files_to_tiff(token, fmt, zoom, x_start, x_stop, y_start, y_stop, file_array):
    # Because we downloaded these files in sequence by z-index
    # (which is bad, it's better to mosaic the coords in x & y as well)
    # we can simply 'slice' them into individual tiff files so they're 1
    # unit 'thick' (like a virtual microtome.)
    i = 1
    print("Converting HDF5 files to single-layer TIFFs.")
    for hdf_file in file_array:
        print("Slicing " + hdf_file)
        f = h5py.File(hdf_file, "r")
        # OCP stores data inside the 'cutout' h5 dataset
        data_layers = f.get('CUTOUT')
        for layer in data_layers:
            # Filename is formatted like the request URL but `/` is `-`
            tiff_file = "-".join([
                token, fmt, str(zoom),
                str(x_start) + "," + str(x_stop),
                str(y_start) + "," + str(y_stop),
                str(i)
            ]) + ".tiff"

            convert.tiff.export_tiff("tiff/" + tiff_file, layer)
            print(".", end="")
            i += 1
        print("\n")



def _download_data(server, token, fmt, zoom, x_start, x_stop, y_start, y_stop, z_start, z_stop, location):
    """
    Download the actual data from the server. Uses 1MB chunks when saving.
    Returns the filename stored locally. Specify a save-location target in get_data.
    """
    print("Downloading " + str(z_start) + "-" + str(z_stop))
    # Build a string that holds the full URL to request.

    request_data = [
        server, 'ocp', 'ca',        # Boilerplate server URL
        token, fmt, str(zoom),      # Set token, format, and zoom
        str(x_start) + "," + str(x_stop),# X
        str(y_start) + "," + str(y_stop),# Y
        str(z_start) + "," + str(z_stop),# Z
        ""                          # Trailing '/'
    ]

    request_url = '/'.join(request_data)
    file_name   = location + "/" + '-'.join(request_data[3:-1]) + "." + fmt

    # Create a `requests` object.
    req = requests.get(request_url, stream=True)
    # Now download (chunking to 1024 bytes from the stream)
    with open(file_name, 'wb+') as f:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()

    return file_name
