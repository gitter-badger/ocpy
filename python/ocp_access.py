import requests


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
    server: Internet-facing server
    token:  Token to identify data to download
    fmt:    The desired output format (see ocp_Convert repository to convert locally)
    zoom:   Zoom level (starts at 0)
    Q_lo:   The lower bound of dimension 'Q'
    Q_hi:   The upper bound of dimension 'Q'
    """

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
                            z_lo, z_hi, location)
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
                            z_last, z_hi, location)
                )
            else:
                # Download from z_last to z_last + CHUNK_DEPTH
                local_files.append(
                    _download_data(server, token, fmt, zoom,
                            x_lo, x_hi,
                            y_lo, y_hi,
                            z_last, z_last + CHUNK_DEPTH, location)
                )

            z_last += CHUNK_DEPTH + 1

    # We now have an array, `local_files`, holding all of the
    # files that we downloaded.

    print [i for i in local_files]



def _download_data(server, token, fmt, zoom, x_lo, x_hi, y_lo, y_hi, z_lo, z_hi, location):
    """
    Download the actual data from the server. Uses 1MB chunks when saving.
    Returns the filename stored locally. Specify a save-location target in get_data.
    """

    # Build a string that holds the full URL to request.

    request_data = [
        server, 'ocp', 'ca',        # Boilerplate server URL
        token, fmt, str(zoom),      # Set token, format, and zoom
        str(x_lo) + "," + str(x_hi),# Z
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

