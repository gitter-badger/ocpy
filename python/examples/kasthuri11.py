import ocpaccess.download

# A few hundred megabytes of the kasthuri11 dataset.
ocpaccess.download.get_data(
        token =     "kasthuri11",
        x_start =      5000,              x_stop =      5500,
        y_start =      5000,              y_stop =      5500,
        z_start =      1,                 z_stop =      3,
        location =  "sample_data"
)


# The code below downloads the full kasthuri11 dataset.
"""
ocpaccess.download.get_data(
        token =     "kasthuri11",
        x_start =      0,              x_stop =      10752,
        y_start =      0,              y_stop =      13312,
        z_start =      1,              z_stop =      1850,
        location =  "data"
)
"""
