# ocpAccess
Scripts to get data from the OCP server. Feel free to submit bug reports [here](https://github.com/openconnectome/ocpAccess/issues).


# Python
These scripts are written to work with 2.7 and (ideally, but untestedly) Python 3. An example (how to download the [*CELL*, Kasthuri (July 30 2015)](http://www.openconnectomeproject.org/#!kasthuri11/c12r2) data) is included inside [`/examples`](https://github.com/openconnectome/ocpAccess/tree/master/python/examples).

In order to set up the python environment, you'll need to download a few libraries. You can use `pip` for this, and run `pip install -r requirements` from inside the `/python` directory, or you can manually install each of the libraries listed in the `requirements` file.

# bash
This provides a function that wraps `curl` in order to allow more efficient chunking and more reliable download than simply trying to download the full dataset simultaneously. Use the file included in [`/examples`](https://github.com/openconnectome/ocpAccess/tree/master/bash/examples) to download the Kasthuri *CELL* 2015 data.

This relies on `curl`, which comes standard on unix and OSX distributions. Windows users are encouraged to use another download method, or may try using `cygwin` for a semi-native `curl` implementation.
