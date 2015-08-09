from __future__ import print_function
import requests, h5py, os, numpy
from PIL import Image

import ocpconvert


DEFAULT_SERVER =    'http://openconnecto.me'
DEFAULT_FORMAT =    'hdf5'
DEFAULT_ZOOM   =    1
CHUNK_DEPTH    =    16

def get_data(token,
             x_lo, x_hi,
             y_lo, y_hi,
             z_lo, z_hi,
             fmt=DEFAULT_FORMAT,
             zoom=DEFAULT_ZOOM,
             server=DEFAULT_SERVER,
             location="./"):
    """
    Get data from the OCP server.
    server:     Internet-facing server
    token:      Token to identify data to download
    fmt:        The desired output format (see ocp_Convert repository to convert locally)
    zoom:       Zoom level (starts at 0)
    Q_lo:       The lower bound of dimension 'Q'
    Q_hi:       The upper bound of dimension 'Q'
    location:   The on-disk location where we'll create /hdf5 and /tiff
    """

    total_size = (x_hi - x_lo) * (y_hi - y_lo) * (z_hi - z_lo) * (14./(1000.*1000.*16.))

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

    confirm = raw_input("The data will be saved to /" + location + ".\n" +
          "Continue? [yn] ")

    if confirm is 'n':
        return;

    fmt = "hdf5" # Hard-coded for now to minimize server-load

    # The array of local files that we create
    local_files = []

    # OCP stores cubes of z-size = CHUNK_DEPTH. To be efficient,
    # we'll download in CHUNK_DEPTH-z-slice units.
    if z_hi - z_lo <= CHUNK_DEPTH:
        # We don't have to split, just download.
        local_files.append(
            _download_data(server, token, fmt, zoom,
                            x_lo, x_hi,
                            y_lo, y_hi,
                            z_lo, z_hi, "hdf5")
        )
    else:
        # We need to split into CHUNK_DEPTH-slice chunks.
        z_last = z_lo
        while z_last < z_hi:
            # Download from z_last to z_last + CHUNK_DEPTH OR
            # z_hi, whichever is smaller
            if z_hi <= z_last + CHUNK_DEPTH:
                # Download from z_last to z_hi
                local_files.append(
                    _download_data(server, token, fmt, zoom,
                            x_lo, x_hi,
                            y_lo, y_hi,
                            z_last, z_hi, "hdf5")
                )
            else:
                # Download from z_last to z_last + CHUNK_DEPTH
                local_files.append(
                    _download_data(server, token, fmt, zoom,
                            x_lo, x_hi,
                            y_lo, y_hi,
                            z_last, z_last + CHUNK_DEPTH, "hdf5")
                )

            z_last += CHUNK_DEPTH + 1

    # We now have an array, `local_files`, holding all of the
    # files that we downloaded.
    # print([i for i in local_files])
    convert_files_to_tiff(token, fmt, zoom, x_lo, x_hi, y_lo, y_hi, local_files)


def convert_files_to_tiff(token, fmt, zoom, x_lo, x_hi, y_lo, y_hi, file_array):
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
                str(x_lo) + "," + str(x_hi),
                str(y_lo) + "," + str(y_hi),
                str(i)
            ]) + ".tiff"

            ocpconvert.tiff.export_tiff(tiff_file, layer)
            print(".", end="")
            i += 1
        print("\n")






def _download_data(server, token, fmt, zoom, x_lo, x_hi, y_lo, y_hi, z_lo, z_hi, location):
    """
    Download the actual data from the server. Uses 1MB chunks when saving.
    Returns the filename stored locally. Specify a save-location target in get_data.
    """
    print("Downloading " + str(z_lo) + "-" + str(z_hi))
    # Build a string that holds the full URL to request.

    request_data = [
        server, 'ocp', 'ca',        # Boilerplate server URL
        token, fmt, str(zoom),      # Set token, format, and zoom
        str(x_lo) + "," + str(x_hi),# X
        str(y_lo) + "," + str(y_hi),# Y
        str(z_lo) + "," + str(z_hi),# Z
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
