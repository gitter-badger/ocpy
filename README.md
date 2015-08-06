# ocpAccess
Scripts to get data from the OCP server. Feel free to submit bug reports [here](https://github.com/openconnectome/ocpAccess/issues).


# Python
These scripts are written to work with 2.7 and (ideally, but untestedly) Python 3. An example (how to download the [*CELL*, Kasthuri (July 30 2015)](http://www.openconnectomeproject.org/#!kasthuri11/c12r2) data) is included inside [`/examples`](https://github.com/openconnectome/ocpAccess/tree/master/python/examples).

In order to set up the python environment, you'll need to download a few libraries. You can use `pip` for this, and run `pip install -r requirements` from inside the `/python` directory, or you can manually install each of the libraries listed in the `requirements` file.

## Python: Usage
The python script `ocp_access.py` contains a function called `get_data`. This is usable from your code: Simply copy this file into your project directory and add `import ocp_access` to the list of python imports.

You can now use the function `ocp_access.get_data()` to retrieve data from the OCP servers.

| Argument | Required | Description |
|----------|----------|-------------|
| `token` | Yes | The project token to download. |
| `x_lo` | Yes | The low bound in dimension X |
| `x_hi` | Yes | The high bound in dimension X |
| `y_lo` | Yes | The low bound in dimension Y |
| `y_hi` | Yes | The high bound in dimension Y |
| `z_lo` | Yes | The low bound in dimension Z |
| `z_hi` | Yes | The high bound in dimension Z |
| `fmt` | No (`hdf5`) | The format in which to download code. (Currently only `hdf5` is legal.) |
| `zoom` | No (`1`) | The zoom level at which to download data |
| `server` | No (`http://openconnecto.me`) | The server at which to request data |
| `location` | No (`./`) | The location on-disk (locally) where you'd like to save the data. Two subdirectories will be created: `/hdf5` and `/tiff`. |

## Python: Example

```
import ocp_access

ocp_access.get_data(
        token =     "kasthuri11",
        x_lo =      5000,              x_hi =      5500,
        y_lo =      5000,              y_hi =      5500,
        z_lo =      1,                 z_hi =      3,
        location =  "data"
)
```

The above script downloads 500x500x2 voxels of data from the `kasthuri11` dataset and saves them on your hard-drive inside a subdirectory called `data`.

**Note:** There is a known bug in the scipy/PIL TIFF converter that prevents accurate hdf5-tiff conversion of non-uint8 data. This will not affect `kasthuri11`.


# bash
This provides a function that wraps `curl` in order to allow more efficient chunking and more reliable download than simply trying to download the full dataset simultaneously. Use the file included in [`/examples`](https://github.com/openconnectome/ocpAccess/tree/master/bash/examples) to download the Kasthuri *CELL* 2015 data.

This relies on `curl`, which comes standard on unix and OSX distributions. Windows users are encouraged to use another download method, or may try using `cygwin` for a semi-native `curl` implementation.
