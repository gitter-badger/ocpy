from PIL import Image
import numpy
import os

def import_tiff(tiff_filename):
    """
    Import a TIFF file into a numpy array.

    Arguments:
        tiff_filename:  A string filename of a TIFF datafile

    Returns:
        A numpy array with data from the TIFF file
    """

    # Expand filename to be absolute
    tiff_filename = os.path.expanduser(tiff_filename)

    try:
        img = Image.open(tiff_filename)
    except Exception as e:
        print("Could not load file {0} for conversion.".format(tiff_filename))
        raise

    return numpy.array(img)



def export_tiff(tiff_filename, numpy_data):
    """
    Export a numpy array to a TIFF file.

    Arguments:
        tiff_filename:  A filename to which to save the TIFF data
        numpy_data:     The numpy array to save to TIFF

    Returns:
        String. The expanded filename that now holds the TIFF data
    """

    # Expand filename to be absolute
    tiff_filename = os.path.expanduser(tiff_filename)

    if numpy_data.dtype is not 'uint8':
        print("Datatype is not uint8, you may experience a known PIL bug. Continuing...")

    if os.path.exists(tiff_filename):
        print("File {0} already exists, stopping...".format(tiff_filename))
        return False

    try:
        img = Image.fromarray(numpy_data)
        img.save(tiff_filename)
    except Exception as e:
        print("Could not save TIFF file {0}.".format(tiff_filename))

    return tiff_filename



def export_tiff_collection(tiff_filename_base, numpy_data, start_layers_at=1):
    """
    Export a numpy array to a set of TIFF files, with each Z-index 2D
    array as its own 2D file.

    Arguments:
        tiff_filename_base:     A filename template, such as "my-image-*.tiff"
                                which will lead to a collection of files named
                                "my-image-0.tiff", "my-image-1.tiff", etc.
        numpy_data:             The numpy array data to save to TIFF.

    Returns:
        Array. A list of expanded filenames that hold TIFF data.
    """

    file_extension = tiff_filename_base.split('.')[-1]
    if file_extension in ['tif', 'tiff']:
        # Filename is "name*.tif[f]", set file_base to "name*".
        file_base = '.'.join(tiff_filename_base.split('.')[:-1])
    else:
        # Filename is "name*", set file_base to "name*".
        # That is, extension wasn't included.
        file_base = tiff_filename_base
        file_extension = ".tiff"

    file_base_array = file_base.split('*')

    # The array of filenames to return
    output_files = []

    i = start_layers_at
    for layer in numpy_data:
        layer_filename = str(i).join(file_base_array) + file_extension
        output_files.append(export_tiff(layer_filename, layer))
        i += 1

    return output_files
