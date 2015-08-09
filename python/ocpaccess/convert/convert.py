import os

FILE_FORMATS = {
    # Format.lower()    # File extension. By convention, use the first by default
    'hdf5':             ['hdf5', 'h5', 'hdf'],
    'tiff':             ['tiff', 'tif'],
    'ramon':            ['m'],
    'matlab':           ['m', 'mat'],
}


# This is not simply FILE_FORMATS in 'reverse', because while we may be able
# to get the file extension for a RAMON object (.m) we can't guess a datatype
# from the ambiguous extension ".m".


def _get_extension_for_format(fmt):
    """
    Get the appropriate file extension for a given format.

    Arguments:
        fmt:        The format to find an extension for

    Returns:
        String. The format (without leading period),
                or False if none was found.
    """
    if fmt in FILE_FORMATS:
        # Use first file extension by default
        return FILE_FORMATS[fmt][0]

    # Otherwise, we don't recognize the format...
    return False



def _guess_format_from_extension(ext):
    """
    Guess the appropriate data type from file extension.

    Arguments:
        ext:        The file extension (period optional)

    Returns:
        String. The format (without leading period),
                or False if none was found or couldn't be guessed
    """
    ext = ext.strip('.')

    # We look through FILE_FORMATS for this extension.
    # - If it appears zero times, return False. We can't guess.
    # - If it appears once, we can simply return that format.
    # - If it appears more than once, we can't guess (it's ambiguous,
    #   e.g .m = RAMON or MATLAB)

    formats = []
    for fmt in FILE_FORMATS:
        if ext in FILE_FORMATS[fmt]:
            formats.append(fmt)

    if formats == [] or len(formats) > 1:
        return False

    return formats[0]




def convert(in_file, out_file, in_fmt="", out_fmt=""):
    """
    Converts in_file to out_file, guessing datatype in the absence of
    in_fmt and out_fmt.

    Arguments:
        in_file:    The name of the (existing) datafile to read
        out_file:   The name of the file to create with converted data
        in_fmt:     Optional. The format of incoming data, if not guessable
        out_fmt:    Optional. The format of outgoing data, if not guessable

    Returns:
        String. Output filename
    """

    if in_fmt == "":
        # Guess in_fmt from in_file
        in_fmt = in_file.slice('.')[-1]
