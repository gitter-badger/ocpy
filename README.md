# ocpAccess
Scripts to get data from the OCP server


# Python
These scripts are written to work with 2.7 and (ideally, but untestedly) Python 3. An example (how to download the [*CELL*, Kasthuri (July 30 2015)](http://www.openconnectomeproject.org/#!kasthuri11/c12r2) data) is included inside [`/examples`](https://github.com/openconnectome/ocpAccess/tree/master/python/examples).

# bash
This provides a function that wraps `curl` in order to allow more efficient chunking and more reliable download than simply trying to download the full dataset simultaneously. Use the file included in [`/examples`](https://github.com/openconnectome/ocpAccess/tree/master/bash/examples) to download the Kasthuri *CELL* 2015 data.
