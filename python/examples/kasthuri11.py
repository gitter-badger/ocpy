import ocpaccess.download

# A few hundred megabytes of the kasthuri11 dataset.
ocpaccess.download.get_data(
        token =     "kasthuri11",
        x_lo =      5000,              x_hi =      5500,
        y_lo =      5000,              y_hi =      5500,
        z_lo =      1,                 z_hi =      3,
        location =  "sample_data"
)


# The code below downloads the full kasthuri11 dataset.
"""
ocpaccess.download.get_data(
        token =     "kasthuri11",
        x_lo =      0,              x_hi =      10752,
        y_lo =      0,              y_hi =      13312,
        z_lo =      1,              z_hi =      1850,
        location =  "data"
)
"""
