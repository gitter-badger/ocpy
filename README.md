# OCPy
Scripts to get data from the OCP server. Feel free to submit bug reports or feature requests [here](https://github.com/openconnectome/ocpAccess/issues).

These scripts are written to work with 2.7 and (ideally, but untestedly) Python 3. An example (how to download the [*CELL*, Kasthuri (July 30 2015)](http://www.openconnectomeproject.org/#!kasthuri11/c12r2) data) is included inside [`/examples`](https://github.com/openconnectome/ocpAccess/tree/master/ocpy/examples).




## Setup
Use `pip` to install the latest stable `ocpy` package from the Python Package Index:

```
pip install ocpy
```

You may need to satisfy requirements as listed in the `requirements` file: You can use `pip` for this as well, and run `pip install -r requirements` from inside the package directory, or you can manually install each of the libraries listed in the `requirements` file.

## Usage
You can use the function `ocpy.access.get_data()` to retrieve data from the OCP servers.

| Argument | Required | Description |
|----------|----------|-------------|
| `token` | Yes | The project token to download. |
| `x_start` | Yes | The low bound in dimension X |
| `x_stop` | Yes | The high bound in dimension X |
| `y_start` | Yes | The low bound in dimension Y |
| `y_stop` | Yes | The high bound in dimension Y |
| `z_start` | Yes | The low bound in dimension Z |
| `z_stop` | Yes | The high bound in dimension Z |
| `fmt` | No (`hdf5`) | The format in which to download code. (Currently only `hdf5` is legal.) |
| `resolution` | Yes | The resolution level at which to download data |
| `server` | No (`http://openconnecto.me`) | The server at which to request data |
| `location` | No (`./`) | The location on-disk (locally) where you'd like to save the data. Two subdirectories will be created: `/hdf5` and `/tiff`. |

See the [guide](#) for more examples and use cases.

## Example

```
import ocpy.access

ocpy.access.get_data(
        token =        "kasthuri11",
        x_start =      5000,              x_stop =      5500,
        y_start =      5000,              y_stop =      5500,
        z_start =      1,                 z_stop =      3,
        location =     "data"
)
```

The above script downloads 500x500x2 voxels of data from the `kasthuri11` dataset and saves them on your hard-drive inside a subdirectory called `data`.

**Note:** There is a known bug in the scipy/PIL TIFF converter that prevents accurate hdf5-tiff conversion of non-uint8 data.

<small>This package was generated using [this tutorial](http://peterdowns.com/posts/first-time-with-pypi.html).</small>
